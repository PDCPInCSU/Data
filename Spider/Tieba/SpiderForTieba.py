# -*- coding: utf-8 -*-
import os
import urllib
import urllib2
import re
import threading
import time
import requests
# 测试用，后边可以删掉，因为肯定抓和分析处理是两个进程的
from TiebaContentAnalysis import *


class SpiderForTieba:

    def __init__(self, owner, target, timer, pageRange):
        # 爬虫的用户
        self.__owner = owner
        self.__target = target
        self.__contentAnalysis = TiebaContentAnalysis(owner, target)
        self.__mapMutex = threading.RLock()
        self.__map = [set(''), set(''), set('')]
        self.__headers = None
        self.__cookieTimeOut = True
        self.__timer = timer
        self.__timerFlag= [True, True]
        self.__timerFlagNum = 0
        # self.__pageRange = pageRange
        try:
            if not os.path.exists('../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'+target):
                os.makedirs('../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'+target)
        except IOError as err:
            print "Error in creating file Path: ../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/"+target
            print "Error is " + str(err)
        # 开始运行
        self.changeTimerAndPageRange(timer=timer, pageRange=pageRange)

    #  唯一一个对外开放的，用来调整Timer
    def changeTimerAndPageRange(self, timer, pageRange):
        self.__timer = timer
        self.__timerFlagNum = (self.__timerFlagNum + 1) % 2
        self.__timerFlag[(self.__timerFlagNum+1)%2] = False
        self.__timerFlag[self.__timerFlagNum] = True
        self.__pageController(pageRange= pageRange, flagNum= self.__timerFlagNum)

    # 我在这里之所以考虑简单粗暴的将While的flag改为self.__flag，主要是考虑到了
    # 在实际过程中，pageRange不可能那么大，所以才这样，不过后边的话我感觉应该会有
    # 更好的办法的
    def __pageController(self, pageRange, flagNum):
        setNum = 0
        while self.__timerFlag[flagNum]:
            for count in range(1, pageRange+1):
                t = threading.Thread(target=self.__getIndex, args=(count, setNum%3))
                t.start()
            setNum += 1
            time.sleep(self.__timer)


    def __openURL(self, url):
        flag = True
        response = None
        if self.__cookieTimeOut:
            conn = requests.session()
            resp = conn.get(url)
            self.__headers = resp.request.headers
            self.__headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4"
            self.__headers['Accept-Encoding'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            self.cookieTimeOut = False
        while flag:
            try:
                request = urllib2.Request(url, headers=self.__headers)
                response = urllib2.urlopen(request)
                flag = False
            except IOError:
                print "Error in opening URL "+ url
                pass
        return response.read()


    # 对相应的首页页面
    def __getIndex(self, pageNum, setNum):
        url = "http://tieba.baidu.com/f?kw=" + urllib.quote(self.__target) + "&ie=utf-8&pn=" + str(50 * (pageNum-1))
        print url
        try:
            content = self.__openURL(url)
        except IOError as err:
            print "Error in opening url : "+ url
            print "Error is " + err
            # 不知道该Return什么0.0 其实应该是这个直接结束的
            return
        patternForIndex = '=\"/p/(\d+)'
        result = re.findall(patternForIndex, content)
        self.__mapMutex.acquire()
        for count in range(0,len(result)):
            if result[count] not in self.__map[setNum] :# 注意，正在修改
                self.__map[setNum].add(result[count])
                t = threading.Thread(target=self.__getThreadContent, args=(result[count],))
                t.start()
        self.__mapMutex.release()
        print len(self.__map[setNum])

        # print len(result)# 用于调试self.__map

    def __getThreadContent(self, urlString):
        try:
            url = 'http://tieba.baidu.com/p/' + urlString
            content = self.__openURL(url)
            # 获取页面数
            pattern = re.compile('pn=(?P<pageNum>\d+)">尾页</a>')
            pageNumResult = re.search(pattern, content)
            if pageNumResult is not None:
                pageNum = int(pageNumResult.group('pageNum'))
            else:
                pageNum = 1
            self.__createCacheFile(urlString, content)
            # 对于多页面帖子：
            count = 1
            while count != pageNum:
                count += 1
                url = 'http://tieba.baidu.com/p/' + urlString + '?pn=' + str(count)
                content = self.__openURL(url)
                self.__createCacheFile(urlString, content)


        except IOError as err :
            print "Error in opening Tieba " + urlString
            print "Error is " + str(err)

    # 将相应的爬下来的内容写入Cache文件
    def __createCacheFile(self, name, content):
        dirPath = '../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'+self.__target + '/'
        filePath = dirPath + name
        try:
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            cacheFile = open(filePath, 'a+')
            cacheFile.writelines(content)
        except IOError as err:
            print "Error is " + str(err)
            print "Error in Creating or writing into Data/Cache/SpiderCache/TiebaCache/Analysing Cache/"+self.__target + '/' +name
        finally:
            if 'cacheFile' in locals():
                cacheFile.close()




test = SpiderForTieba(owner=0, target='刀剑神域', timer=5, pageRange=2)