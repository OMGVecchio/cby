#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import bs4
import re
from bs4 import BeautifulSoup

class Tool(object):

    def __init__(self, url = '/wechat/search.html', host = 'https://www.chuanboyi.com'):
        res = urllib2.urlopen(host + url)
        htmlRaw = res.read()
        self.html = BeautifulSoup(htmlRaw, 'html.parser')

    def loadHtml(self, url = '/wechat/search.html', host = 'https://www.chuanboyi.com', page = 0):
        if page != 0:
            newUrl = re.sub(r'.html$', '-page-' + str(page) + '.html', url)
        else:
            newUrl = url
        res = urllib2.urlopen(host + newUrl)
        htmlRaw = res.read()
        return BeautifulSoup(htmlRaw, 'html.parser')

    def getContent(self, html, catName):
        content = html.select('.news_content tr')
        # 抓取 微信 > 所有
        resData = []
        if catName == 'wechat':
            resData = self.__wechat__(content)
        elif catName == 'weibo':
            resData = self.__weibo__(content)
        elif catName == 'video':
            resData = self.__video__(content)
        elif catName == 'zimeiti':
            resData = self.__zimeiti__(content)
        elif catName == 'news':
            resData = self.__news__(content)
        elif catName == 'ad':
            resData = self.__ad__(content)
        elif catName == 'wlyx':
            resData = self.__wlyx__(content)
        elif catName == 'wach':
            resData = self.__wach__(content)
        elif catName == 'act':
            resData = self.__act__(content)
        elif catName == 'zanzhu':
            resData = self.__zanzhu__(content)
        elif catName == 'haiwai':
            resData = self.__haiwai__(content)
        
        return resData

    # 获取 微信 数据
    def __wechat__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            fans = list(item.select('td')[5].stripped_strings)
            obj = {'name': name, 'fans': fans[0]}
            data.insert(index, obj)
        return data
    
    # 获取 微博 数据
    def __weibo__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            fans = list(item.select('td')[3].stripped_strings)
            obj = {'name': name, 'fans': fans[0]}
            data.insert(index, obj)
        return data

    # 获取 视频 数据
    def __video__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            fans = list(item.select('td')[4].stripped_strings)
            obj = {'name': name, 'fans': fans[0]}
            data.insert(index, obj)
        return data

    # 获取 自媒体 数据
    def __zimeiti__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            fans = list(item.select('td')[4].stripped_strings) or [0]
            obj = {'name': name, 'fans': fans[0]}
            data.insert(index, obj)
        return data

    # 获取 软文 数据
    def __news__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            cat = list(item.select('td')[2].stripped_strings)
            obj = {'name': name, 'category': cat[0]}
            data.insert(index, obj)
        return data

    # 获取 广告 数据
    def __ad__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            cat = list(item.select('td')[2].stripped_strings)
            obj = {'name': name, 'category': cat[0]}
            data.insert(index, obj)
        return data

    # 获取 网络营销 数据
    def __wlyx__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            cat = list(item.select('td')[2].stripped_strings) or ['']
            obj = {'name': name, 'category': cat[0]}
            data.insert(index, obj)
        return data

    # 获取 文案策划 数据
    def __wach__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            cat = list(item.select('td')[2].stripped_strings)
            obj = {'name': name, 'category': cat[0]}
            data.insert(index, obj)
        return data

    # 获取 活动服务 数据
    def __act__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            cat = list(item.select('td')[2].stripped_strings)
            obj = {'name': name, 'category': cat[0]}
            data.insert(index, obj)
        return data

    # 获取 广告招标 数据
    def __zanzhu__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            cat = list(item.select('td')[2].stripped_strings)
            obj = {'name': name, 'category': cat[0]}
            data.insert(index, obj)
        return data
    
    # 获取 海外营销 数据
    def __haiwai__(self, html):
        data = []
        for index in range(len(html)):
            item = html[index]
            name = self.__getAccountName__(item)
            cat = list(item.select('td')[3].stripped_strings)
            obj = {'name': name, 'category': cat[0]}
            data.insert(index, obj)
        return data

    def __getAccountName__(self, item):
        nameSet = item.select('.account_name')[0]
        if type(nameSet) == bs4.element.NavigableString:
            return nameSet
        else:
            for key in nameSet.children:
                if type(key) == bs4.element.NavigableString:
                    return key
                else:
                    print('--key--')
                    print(key)
                    for tag in key:
                        print('--tag--')
                        print(tag)
                        if type(tag) == bs4.element.NavigableString:
                            return tag

    # 获取某类目总页数
    def getTotalPage(self, html):
        tagName = '.pagination li a'
        paginationList = html.select(tagName)
        currCount = len(paginationList)
        if currCount == 0:
            return 1
        else:
            lastTag = paginationList[currCount - 1]
            if lastTag.has_attr('rel'):
                totalPage = paginationList[currCount - 2].attrs['data-ci-pagination-page']
            elif lastTag.has_attr('data-ci-pagination-page'):
                totalPage = lastTag.attrs['data-ci-pagination-page']
            else:
                totalPage = lastTag.string
            return int(totalPage)

    # 获取 总类目 列表
    def getCategory(self, html):
        tagName = '.aw-top-nav li a'
        catList = html.select(tagName)
        catUrlList = []
        for index in range(len(catList)):
            cat = catList[index]
            href = cat.attrs['href']
            catUrlList.insert(index, href)
        return catUrlList

    # 获取 所有分类 代表的链接
    def getAllUrl(self, html):
        tagName = '.hyfl_tags'
        allTags = html.select(tagName)
        allTag = allTags[0]
        return allTag.attrs['href']
