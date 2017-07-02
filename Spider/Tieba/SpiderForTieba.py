# -*- coding: utf-8 -*-
import os
import urllib
import urllib2
import re
# 测试用，后边可以删掉，因为肯定抓和分析处理是两个进程的
from TiebaContentAnalysis import *


class SpiderForTieba:

    def __init__(self, owner, target):

        # 爬虫的用户
        self.owner = owner
        self.target = urllib.quote(target)
        self.file = None
        self.contentAnalysis = TiebaContentAnalysis()

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
        print self.contentAnalysis.readCacheFile(urlString)

    # 将相应的爬下来的内容写入Cache文件
    def createCacheFile(self, name, content):

        dirPath = '../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'
        filePath = dirPath + name
        try:
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            cacheFile = open(filePath, 'a+')
            cacheFile.writelines(content)
        except IOError as err:
            print "Error is " + err
            print "Error in Creating or writing into Data/Cache/SpiderCache/TiebaCache/Analysing Cache/" + name
        finally:
            if 'cacheFile' in locals():
                cacheFile.close()




test = SpiderForTieba(0, '中南大学')
test.getThreadContent('5181822218')
