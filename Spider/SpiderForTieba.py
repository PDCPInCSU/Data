# -*- coding: utf-8 -*-

import urllib2
import re

from ContentAnalysis import ContentAnalysis


class SpiderForTieba:

    def __init__(self, owner, target):

        # 爬虫的用户
        self.owner = owner
        # 爬虫
        self.target = target
        self.file = None
        self.contentAnalysis = ContentAnalysis()

    def openURL(self, url):

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        return response.read()

    def getIndex(self):

        url = "http://tieba.baidu.com/f?kw=" + self.target
        content = self.openURL(url)
        pattern = '(?:="/)(?:/tieba\.baidu\.com)?/p/(\d+)'
        result = re.findall(pattern, content)

        return result

    def getThreadContent(self, urlString):

        url = "http://tieba.baidu.com/p/" + urlString
        content = self.openURL(url)

        print content
    # def get

test = SpiderForTieba(0, "中南大学")
test.getContent()
