# _*_ coding: utf-8 _*_
"""
作者:qtwaiter
日期:2020年12月27日

"""
import pandas
dfs = pandas.read_html('https://www.boc.cn/sourcedb/whpj/')
#print(dfs)
type(dfs)
len(dfs)
print(len(dfs))
currency = dfs[1]

currency = currency.iloc[6:13]
print(currency)
currency.to_excel('currency.xlsx')