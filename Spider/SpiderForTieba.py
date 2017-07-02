# -*- coding: utf-8 -*-
import sys
import os
import urllib
import urllib2
import re


# from ContentAnalysis import ContentAnalysis


class SpiderForTieba:

    def __init__(self, owner, target):

        # 爬虫的用户
        self.owner = owner
        # 爬虫
        # self.target = urllib.urlencode(target)

        self.target = urllib.quote(target)
        self.file = None
        # self.contentAnalysis = ContentAnalysis()
        print  self.target
    def openURL(self, url):

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        return response.read()

    # def pageController(self):

    def getIndex(self, pageNum):

        url = "http://tieba.baidu.com/f?kw=" + self.target + "ie=utf-8&pn=" + str(50 * pageNum-1)
        content = self.openURL(url)
        patternForIndex = '(?:="/)(?:/tieba\.baidu\.com)?/p/(\d+)'
        result = re.findall(patternForIndex, content)



    def getThreadContent(self, urlString):

        url = "http://tieba.baidu.com/p/" + urlString
        content = self.openURL(url)
        self.createCacheFile(urlString, content)
        # print content

    def createCacheFile(self, name, content):

        dirPath = '../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'
        filePath = dirPath + name
        try:
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            cacheFile = open(filePath, 'a+')
            cacheFile.writelines(content)
        except IOError as err:
            print "Error in Creating or Opening file " + name
            print "Error is " + err
        finally:
            if 'cacheFile' in locals():
                cacheFile.close()



test = SpiderForTieba(0, '中南大学')
test.getThreadContent('5181822218')
