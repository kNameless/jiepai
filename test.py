from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

import requests
import json
import re


# a = 'gallery: JSON.parse("{\"count\":7,\"sub_images\":[{\"url\":\"http:\\/\\/p3.pstatp.com\\/origin\\/pgc-image\\/1531377247568a3cd0eb613\",\"width\":640,\"url_list\":[{\"url\":\"http:\\/\\/p3.pstatp.com\\/origin\\/pgc-image\\/1531377247568a3cd0eb613\"},{\"url\":\"http:\\/\\/pb9.pstatp.com\\/origin\\/pgc-image\\/1531377247568a3cd0eb613\"},{\"url\":\"http:\\/\\/pb1.pstatp.com\\/origin\\/pgc-image\\/1531377247568a3cd0eb613\"}],\"uri\":\"origin\\/pgc-image\\/1531377247568a3cd0eb613\",\"height\":963},{\"url\":\"http:\\/\\/p1.pstatp.com\\/origin\\/pgc-image\\/1531377247668ddb835f378\",\"width\":640,\"url_list\":[{\"url\":\"http:\\/\\/p1.pstatp.com\\/origin\\/pgc-image\\/1531377247668ddb835f378\"},{\"url\":\"http:\\/\\/pb3.pstatp.com\\/origin\\/pgc-image\\/1531377247668ddb835f378\"},{\"url\":\"http:\\/\\/pb9.pstatp.com\\/origin\\/pgc-image\\/1531377247668ddb835f378\"}],\"uri\":\"origin\\/pgc-image\\/1531377247668ddb835f378\",\"height\":1050},{\"url\":\"http:\\/\\/p1.pstatp.com\\/origin\\/pgc-image\\/153137724761322a5489eab\",\"width\":640,\"url_list\":[{\"url\":\"http:\\/\\/p1.pstatp.com\\/origin\\/pgc-image\\/153137724761322a5489eab\"},{\"url\":\"http:\\/\\/pb3.pstatp.com\\/origin\\/pgc-image\\/153137724761322a5489eab\"},{\"url\":\"http:\\/\\/pb9.pstatp.com\\/origin\\/pgc-image\\/153137724761322a5489eab\"}],\"uri\":\"origin\\/pgc-image\\/153137724761322a5489eab\",\"height\":959},{\"url\":\"http:\\/\\/p3.pstatp.com\\/origin\\/pgc-image\\/1531377247717e02c7182b0\",\"width\":640,\"url_list\":[{\"url\":\"http:\\/\\/p3.pstatp.com\\/origin\\/pgc-image\\/1531377247717e02c7182b0\"},{\"url\":\"http:\\/\\/pb9.pstatp.com\\/origin\\/pgc-image\\/1531377247717e02c7182b0\"},{\"url\":\"http:\\/\\/pb1.pstatp.com\\/origin\\/pgc-image\\/1531377247717e02c7182b0\"}],\"uri\":\"origin\\/pgc-image\\/1531377247717e02c7182b0\",\"height\":1002},{\"url\":\"http:\\/\\/p1.pstatp.com\\/origin\\/pgc-image\\/1531377247617c4d54a8b2e\",\"width\":640,\"url_list\":[{\"url\":\"http:\\/\\/p1.pstatp.com\\/origin\\/pgc-image\\/1531377247617c4d54a8b2e\"},{\"url\":\"http:\\/\\/pb3.pstatp.com\\/origin\\/pgc-image\\/1531377247617c4d54a8b2e\"},{\"url\":\"http:\\/\\/pb9.pstatp.com\\/origin\\/pgc-image\\/1531377247617c4d54a8b2e\"}],\"uri\":\"origin\\/pgc-image\\/1531377247617c4d54a8b2e\",\"height\":958},{\"url\":\"http:\\/\\/p3.pstatp.com\\/origin\\/pgc-image\\/1531377247619b2ce737413\",\"width\":640,\"url_list\":[{\"url\":\"http:\\/\\/p3.pstatp.com\\/origin\\/pgc-image\\/1531377247619b2ce737413\"},{\"url\":\"http:\\/\\/pb9.pstatp.com\\/origin\\/pgc-image\\/1531377247619b2ce737413\"},{\"url\":\"http:\\/\\/pb1.pstatp.com\\/origin\\/pgc-image\\/1531377247619b2ce737413\"}],\"uri\":\"origin\\/pgc-image\\/1531377247619b2ce737413\",\"height\":1153},{\"url\":\"http:\\/\\/p3.pstatp.com\\/origin\\/pgc-image\\/1531377247675c71b65099e\",\"width\":640,\"url_list\":[{\"url\":\"http:\\/\\/p3.pstatp.com\\/origin\\/pgc-image\\/1531377247675c71b65099e\"},{\"url\":\"http:\\/\\/pb9.pstatp.com\\/origin\\/pgc-image\\/1531377247675c71b65099e\"},{\"url\":\"http:\\/\\/pb1.pstatp.com\\/origin\\/pgc-image\\/1531377247675c71b65099e\"}],\"uri\":\"origin\\/pgc-image\\/1531377247675c71b65099e\",\"height\":960}],\"max_img_width\":640,\"labels\":[\"\\u65f6\\u88c5\\u642d\\u914d\"],\"sub_abstracts\":[\"\\u8857\\u62cd\\u8def\\u4eba\\uff0c\\u590f\\u5929\\u6e05\\u51c9\\u7684\\u51fa\\u884c\\u7a7f\\u642d\\u53c2\\u8003\\uff0c\\u8ba9\\u4f60\\u53d8\\u5f97\\u6e05\\u65b0\\u53c8\\u8131\\u4fd7\",\" \",\" \",\"\\u8857\\u62cd\\u8def\\u4eba\\uff0c\\u590f\\u5929\\u6e05\\u51c9\\u7684\\u51fa\\u884c\\u7a7f\\u642d\\u53c2\\u8003\\uff0c\\u8ba9\\u4f60\\u53d8\\u5f97\\u6e05\\u65b0\\u53c8\\u8131\\u4fd7\",\" \",\" \",\"\\u8857\\u62cd\\u8def\\u4eba\\uff0c\\u590f\\u5929\\u6e05\\u51c9\\u7684\\u51fa\\u884c\\u7a7f\\u642d\\u53c2\\u8003\\uff0c\\u8ba9\\u4f60\\u53d8\\u5f97\\u6e05\\u65b0\\u53c8\\u8131\\u4fd7\"],\"sub_titles\":[\"\\u8857\\u62cd\\u8def\\u4eba\\uff0c\\u590f\\u5929\\u6e05\\u51c9\\u7684\\u51fa\\u884c\\u7a7f\\u642d\\u53c2\\u8003\\uff0c\\u8ba9\\u4f60\\u53d8\\u5f97\\u6e05\\u65b0\\u53c8\\u8131\\u4fd7\",\"\\u8857\\u62cd\\u8def\\u4eba\\uff0c\\u590f\\u5929\\u6e05\\u51c9\\u7684\\u51fa\\u884c\\u7a7f\\u642d\\u53c2\\u8003\\uff0c\\u8ba9\\u4f60\\u53d8\\u5f97\\u6e05\\u65b0\\u53c8\\u8131\\u4fd7\",\"\\u8857\\u62cd\\u8def\\u4eba\\uff0c\\u590f\\u5929\\u6e05\\u51c9\\u7684\\u51fa\\u884c\\u7a7f\\u642d\\u53c2\\u8003\\uff0c\\u8ba9\\u4f60\\u53d8\\u5f97\\u6e05\\u65b0\\u53c8\\u8131\\u4fd7\",\"\\u8857\\u62cd\\u8def\\u4eba\\uff0c\\u590f\\u5929\\u6e05\\u51c9\\u7684\\u51fa\\u884c\\u7a7f\\u642d\\u53c2\\u8003\\uff0c\\u8ba9\\u4f60\\u53d8\\u5f97\\u6e05\\u65b0\\u53c8\\u8131\\u4fd7\",\"\\u8857\\u62cd\\u8def\\u4eba\\uff0c\\u590f\\u5929\\u6e05\\u51c9\\u7684\\u51fa\\u884c\\u7a7f\\u642d\\u53c2\\u8003\\uff0c\\u8ba9\\u4f60\\u53d8\\u5f97\\u6e05\\u65b0\\u53c8\\u8131\\u4fd7\",\"\\u8857\\u62cd\\u8def\\u4eba\\uff0c\\u590f\\u5929\\u6e05\\u51c9\\u7684\\u51fa\\u884c\\u7a7f\\u642d\\u53c2\\u8003\\uff0c\\u8ba9\\u4f60\\u53d8\\u5f97\\u6e05\\u65b0\\u53c8\\u8131\\u4fd7\",\"\\u8857\\u62cd\\u8def\\u4eba\\uff0c\\u590f\\u5929\\u6e05\\u51c9\\u7684\\u51fa\\u884c\\u7a7f\\u642d\\u53c2\\u8003\\uff0c\\u8ba9\\u4f60\\u53d8\\u5f97\\u6e05\\u65b0\\u53c8\\u8131\\u4fd7\"]}"),'
#
#
# images_pattern = re.compile('gallery: JSON.parse.*?({".*?"]}).*?,', re.S)
# result = re.search(images_pattern, a)
# print(result.group(1))

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}


def get_page_detail(url):
    print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页失败', url)
        return None

page = get_page_detail('http://toutiao.com/group/6577608090328236552/')

# urls = findall_in_page(page, 'gallery: JSON.parse("', '"),')
# images_pattern = re.compile('gallery: JSON.parse.*?(.*?).*?,', re.S)
images_pattern = re.compile('gallery: JSON\.parse\("(.*?)"\)',re.S)
result = re.search(images_pattern, page)
goal = re.sub('\\\\', '', result.group(1))
print(result.group(1))
print(goal)


