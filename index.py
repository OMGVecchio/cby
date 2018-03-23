#!/usr/bin/python
# -*- coding:utf-8 -*-
# 传播易

from mongo import CbyMongo
from tools import Tool
import re

mongo = CbyMongo()

# weixin = mongo.getTable('weixin')
# tool = Tool()
# totalPage = tool.getTotalPage()
# for index in range(totalPage):
#     newUrl = '/wechat/search-catid-1-type-price_one-page-' + str( index + 1) + '.html'
#     print(newUrl)
#     newTool = Tool(url = newUrl)
#     newContent = newTool.getContent()
#     print(newContent)
#     weixin.insert_many(newContent)

starter = Tool()
html = starter.loadHtml()
category = starter.getCategory(html)

for cat in category:
    catName = re.findall(r'/([a-zA-Z]*)/search.html', cat)[0]
    if catName == 'zanzhu':
        print(u'--------进入 %s 模块-----------' % catName)
        mongoTool = mongo.getTable(catName)
        catLoader = Tool()
        newHtml = catLoader.loadHtml(url = cat)
        getTotalPage = catLoader.getTotalPage(newHtml)
        allUrl = catLoader.getAllUrl(newHtml)
        for index in range(getTotalPage):        
            page = (index + 1)
            print(u'--------爬取 %s 模块,第 %d 页-----------' % (catName, page))
            subCatLoader = Tool()
            subCatHtml = subCatLoader.loadHtml(url = allUrl, page = page)
            subCatContent = subCatLoader.getContent(subCatHtml, catName)
            print(u'--------存入 %s 模块,第 %d 页-----------' % (catName, page))
            mongoTool.insert_many(subCatContent)
