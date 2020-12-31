# _*_ coding: utf-8 _*_
"""
作者:qtwaiter
日期:2020年12月30日

"""
import tushare as ts
import pandas as pd
ts.set_token('接口token') #访问Tushare社区门户（https://waditu.com），点击右上角“注册”
import datetime
today = datetime.date.today()
formatted_today = today.strftime('%Y%m%d') #大写Y是2020，小写20
yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y%m%d')
pro = ts.pro_api()
#描述：获取新闻联播文字稿数据，数据开始于2006年6月，超过12年历史
#积分：用户积累120积分可以调取，但会做流控限制，超过5000无限制
df = pro.cctv_news(date='20201230')
print(df.values)

df.to_csv('新闻联播{}.csv'.format(yesterday),encoding='utf-8-sig')

#  关于pandas的文件读取和保存格式见官网地址：
#  https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html
# https://tushare.pro/register?reg=413599 分享此链接，成功注册一个有效用户(指真正会使用tushare数据的用户)可获得50积分，虚假用户带来的积分会被定期回收！
