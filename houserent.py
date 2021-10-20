
import requests
import parsel
import csv


#1.目标网址
url = 'https://hz.lianjia.com/ershoufang/pg2/'
#2.发送请求和接收响应
resp = requests.get(url)

#print(resp.text)

#3.解析网页 parsel库
selector = parsel.Selector(resp.text)
Lis = selector.css('.sellListContent Li')
dic = {}

f = open('二手房信息.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f,fieldnames=['标题', '链接', '价格'])
csv_writer.writeheader()

for Li in Lis:
    # 选取 class=title标签
    title = Li.css('.title a::text').get()
    dic['标题'] = title
    Link = Li.css('.title a::attr(href)').get()
    dic['链接'] = Link
    Price = Li.css('.totalPrice span::text').get()
    dic['价格'] = Price
    #print(title)
    csv_writer.writerow(dic)
    print(dic)
#4.保存数据
f.close()
