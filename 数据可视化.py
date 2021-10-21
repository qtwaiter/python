
import json
import requests
import jsonpath #提取数据

from pyecharts.charts import Map #地图绘制
from pyecharts import options as opts
from demo1 import nameMap
url ='https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'

resp = requests.post(url).text

#print(resp)

# 字符串 ---dict字典 数据类型转换

data = json.loads(resp)
#print(type(data))

#从网页源代码提取数据， 名字name+病毒率confirm

name = jsonpath.jsonpath(data, "$..name") # $代表最外层的字典，..name代表匹配的数据
# print(name)

confirm = jsonpath.jsonpath(data, "$..confirm")

# print(confirm)

a = list(zip(name, confirm)) #zip组合数据

# print(type(a))

#以上数据抓取完成

#数据可视化展示，地图绘制
map_ = Map(opts.InitOpts(width='1200px', height='600px')).add(series_name='世界各国疫情', data_pair=a, maptype='world',
                                                              name_map=nameMap, is_map_symbol_show=False)

#不显示国家名称
map_.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#设置颜色 左上角名称 图例
map_.set_global_opts(title_opts=opts.TitleOpts(title="国外疫情状况"), visualmap_opts=opts.VisualMapOpts(max_=40000000))

map_.render("国外疫情.html")