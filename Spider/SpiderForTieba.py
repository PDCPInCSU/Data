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

        print self.readCacheFile(urlString)


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

    # 读取文件，但是如果打开文件失败会返回None
    def readCacheFile(self,name):
        dirPath = '../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'
        filePath = dirPath + name
        result = None
        try:
            cacheFile = open(filePath, 'r')
            result = cacheFile.read()
        except IOError as err:
            print "Error in Reading file Data/Cache/SpiderCache/TiebaCache/Analysing Cache/" + name
            print "Error is " + err
        finally:
            if 'cacheFile' in locals():
                cacheFile.close()
        return result


test = SpiderForTieba(0, '中南大学')
test.getThreadContent('5181822218')
