# -*- coding: utf-8 -*-
import os
class TiebaContentAnalysis:

    def __init__(self, owner, target):
        self.__owner = owner
        self.__target = target

    # 读取文件，但是如果打开文件失败会返回None
    def __readCacheFile(self, name):
        dirPath = '../../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'+self.__target+'/'
        filePath = dirPath + name
        result = None
        print filePath
        try:
            if os.path.exists(filePath):
                cacheFile = open(filePath, 'r')
                result = cacheFile.read()
            else:
                print "File " + self.__target + '/' + name +" doesn't exist"
        except IOError as err:
            print "Error in Reading file Data/Cache/SpiderCache/TiebaCache/Analysing Cache/" +self.__target+'/'+ name
            print "Error is " + str(err)
        finally:
            if 'cacheFile' in locals():
                cacheFile.close()
        return result

    # 控制整个的进程
    # def __analysingController(self, target, timer, numRange):

    # 将每一个文件的内容按照楼层分割，可能会出现文件里边有楼层重复的现象（因为那边）
    def __contentRegularing(self, content):
    #
    #
    #
    # def __getSegmented(self, content):
    #
    #
    # def __getRehulared(self, content):
    #
    # def __getAnalyzed(self, content):
    #
    # def __openURL(self, url):
    #


test = TiebaContentAnalysis(0, '刀剑神域')