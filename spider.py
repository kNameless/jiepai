from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pymongo
from hashlib import md5
import os

from config import*
import requests
import json
import re
from multiprocessing import Pool

client = pymongo.MongoClient(MONGOURL, connect=False)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页失败')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页失败', url)
        return None


def parse_page_detail(html, url):
    print(url)
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    images_pattern = re.compile('gallery: JSON\.parse\("(.*?)"\)', re.S)#“\”保证原本网页代码的符号不被正则表达式所翻译
    result = re.search(images_pattern, html)
    if result:
        goal = re.sub('\\\\', '', result.group(1))
        # print(goal)
        data = json.loads(goal)
        if data and 'sub_images' in data.keys():
            sub_images = data.get("sub_images")
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image, title)
            return {
                'title': title,
                'url': url,
                'images': images,
            }


def sve_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储成功',result)
        return True
    return False


def download_image(url, title):
    print('正在下载', url)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            save_image(response.content, title)
        return None
    except RequestException:
        print('请求图片失败', url)
        return None


def save_image(content, title):
    path = "F:\PyImage\\"+title.split("\\")[-1]
    if not os.path.exists(path):
        # os.mkdir() 方法用于以数字权限模式创建目录。默认的模式为 0777 (八进制)。
        os.mkdir(path)
    file_path = '{0}/{1}.{2}'.format(path, md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            if result:
                sve_to_mongo(result)


if __name__ == '__main__':
    # groups = [x*20 for x in range(GROUP_START, GROUP_END+1)]
    # pool = Pool()
    # pool = [main, groups]
    groups = [x * 20 for x in range(GROUP_START, GROUP_END + 1)]
    i = 0
    for i in groups:
        main(i)