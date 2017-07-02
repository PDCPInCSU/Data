# -*- coding: utf-8 -*-


class TiebaContentAnalysis:

    def __init__(self, owner):
        self.owner = owner

    # 读取文件，但是如果打开文件失败会返回None
    def readCacheFile(self, name):
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
