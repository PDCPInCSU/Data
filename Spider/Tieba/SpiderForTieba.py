# -*- coding: utf-8 -*-
import os
import urllib
import urllib2
import re
import threading
# 测试用，后边可以删掉，因为肯定抓和分析处理是两个进程的
from TiebaContentAnalysis import *


class SpiderForTieba:

    def __init__(self, owner, target):
        # 爬虫的用户
        self.owner = owner
        self.target = target
        self.contentAnalysis = TiebaContentAnalysis(owner, target)
        self.mapMutex = threading.RLock()
        self.map = set()
        try:
            if not os.path.exists('../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'+target):
                os.makedirs('../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'+target)
        except IOError as err:
            print "Error in creating file Path: ../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/"+target
            print "Error is " + str(err)

    def openURL(self, url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()

    # def pageController(self):

    def getIndex(self, pageNum, ):
        url = "http://tieba.baidu.com/f?kw=" + urllib.quote(self.target) + "ie=utf-8&pn=" + str(50 * pageNum-1)
        try:
            content = self.openURL(url)
        except IOError as err:
            print "Error in opening url : "+ url
            # 不知道该Return什么0.0 其实应该是这个直接结束的
            return
        patternForIndex = '=\"/p/(\d+)'
        result = re.findall(patternForIndex, content)
        self.mapMutex.acquire()
        for count in range(0,len(result)):
            # print result[count] # 用于调试self.map
            if result[count] not in self.map:
                self.map.add(result[count])
                t = threading.Thread(target=self.getThreadContent, args=(result[count],))
                t.start()
        self.mapMutex.release()
        # print len(result)# 用于调试self.map

    def getThreadContent(self, urlString):
        try:
            url = 'http://tieba.baidu.com/p/' + urlString
            content = self.openURL(url)
            # 获取页面数
            pattern = re.compile('pn=(?P<pageNum>\d)">尾页</a>')
            pageNumResult = re.search(pattern, content)
            if pageNumResult is not None:
                pageNum = int(pageNumResult.group('pageNum'))
            else:
                pageNum = 1

            self.createCacheFile(urlString, content)
            # 对于多页面帖子：
            count = 1
            while count != pageNum:
                url = 'http://tieba.baidu.com/p/' + urlString + '?pn=' + str(count)
                content = self.openURL(url)
                self.createCacheFile(urlString, content)
                count += 1
        except IOError as err :
            print "Error in opening Tieba " + urlString
            print "Error is " + str(err)

    # 将相应的爬下来的内容写入Cache文件
    def createCacheFile(self, name, content):
        dirPath = '../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'+self.target + '/'
        filePath = dirPath + name
        try:
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            cacheFile = open(filePath, 'a+')
            cacheFile.writelines(content)
        except IOError as err:
            print "Error is " + str(err)
            print "Error in Creating or writing into Data/Cache/SpiderCache/TiebaCache/Analysing Cache/"+self.target + '/' +name
        finally:
            if 'cacheFile' in locals():
                cacheFile.close()




test = SpiderForTieba(0, '中南大学')
test.getIndex(1)
# test.getThreadContent('5181822218')
