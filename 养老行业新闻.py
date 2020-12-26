
# _*_ coding: utf-8 _*_
"""
作者:qtwaiter
日期:2020年12月26日

"""
import requests
from bs4 import BeautifulSoup

url = 'http://www.yanglaocn.com/yanglaoyuan/hangyexinwen/'
html = requests.get(url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"})
html.encoding = 'utf-8'
# print(html)
req = html.text
soup = BeautifulSoup(req, "lxml")
# print(soup)
divs = soup.select('.news_list_ul')
#print(divs)
for div in divs:
    content = div.select_one('a.ameth8')
    url_next = div.select_one('.PageList.PageListTile, a')
    detail_url = url_next.get('href')
    post_date = div.select_one('.PageListTime')

    print(url_next.text)
    print('发布日期：', post_date.text)
    print('内容摘要：', content.text)
    print(detail_url)
