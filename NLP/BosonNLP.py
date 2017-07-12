# -*- coding: utf-8 -*-
from bosonnlp import BosonNLP
import time
import threadpool
import json
import os
class nlp:

    # token 是用户自己申请，或者是通过本平台代理的Boson或者是其他的token
    # sourceType 0是贴吧，1是知乎
    def __init__(self, token, target, sourceType, poolSize, timer):
        self.__token = token
        self.__target = target
        self.__nlp = BosonNLP(token)
        self.__cacheFileSet = set()

        # 因为自身没有Switch，自己也懒得写，反正知乎等其他部分的爬虫没写，
        # 不知道是否Regularized Cache是否需要有其他格式的，就先只写针对目前JSON一种的
        # 为了方便处理位置，就要求输入Type，然后通过Type来确定Regularized Cache的路径了
        if sourceType == 0: # Tieba
            self.__regularizedCachePath = '../Data/Cache/SpiderCache/TiebaCache/Regularized Cache/' + target +'/'
        else: # 否则的话就是Zhihu
            self.__regularizedCachePath = '../Data/Cache/SpiderCache/ZhihuCache/Regularized Cache/' + target +'/'

        self.__analysingController(poolSize, timer)
        # test =  self.__readCacheFile('2283736035')
        # self.__getSegmented(test)

    def __getFileNames(self):
        result = set()
        for root , dirs, files in os.walk(self.__regularizedCachePath):
            for fileName in files:
                result.add(fileName)
        if '.DS_Store' in result:
            result.remove('.DS_Store')
        return result

    def __analysingController(self, poolSize, timer):
        task_pool = threadpool.ThreadPool(poolSize)
        while True:
            self.__cacheFileSet |= self.__getFileNames()
            for eachFile in self.__cacheFileSet:
                print eachFile
                fileContent = self.__readCacheFile(eachFile)
                requestList = threadpool.makeRequests(self.__getFileAnalyzied,
                                                      [(None, {"content":fileContent,"name": eachFile})])
                [task_pool.putRequest(req) for req in requestList]
                task_pool.wait()
            time.sleep(timer)

    def __getFileAnalyzied(self, content,name):
        for eachFloor in content:
            content.update({eachFloor: self.__analysis(content[eachFloor])})
        self.__createCacheFile(name, content)


    # content为JSON格式
    # TODO:处理的时候对楼层只有图片的情况考虑不完善，同时暂时没有考虑水楼的情况
    def __analysis(self, content):
        # 考虑到API是收费的，所以在这里加一个判断来降低没有必要的消耗
        # TODO：这里后期打算把这个判断写为一个函数,因为那些水楼什么的我都没有处理，
        # TODO: 而且封装为一个函数之后，我可以使得各模块后期再加入图片分析功能的时候不用修改太多代码
        if not content["Content"] == ' ':
            # 首先识别类别
            tag ={ "tag": self.__nlp.classify(content["Content"])}
            content.update(tag)
            # 然后是情感分析
            sentiment = {"sentiment": self.__nlp.sentiment(content["Content"])}
            content.update(sentiment)
            # 命名实体分析 这里不想写了
            ner = {"ner": self.__nlp.ner(content["Content"])}
            content.update(ner)
            # 关键词
            keyWords = {"keyWords": self.__nlp.extract_keywords(content["Content"])}
            content.update(keyWords)
        return content

    # 读取文件，但是如果打开文件失败会返回None
    # 直接以JSON读取了
    def __readCacheFile(self, name):
        filePath = self.__regularizedCachePath + name
        result = None
        # print filePath # 调试用
        try:
            if os.path.exists(filePath):
                cacheFile = open(filePath, 'r')
                result = json.load(cacheFile)
            else:
                print "File " + self.__target + '/' + name +" doesn't exist"
        except IOError as err:
            print "Error in Reading file Data/Cache/SpiderCache/TiebaCache/Regularized Cache/" +self.__target+'/'+ name
            print "Error is " + str(err)
        finally:
            if 'cacheFile' in locals():
                cacheFile.close()
        return result

    # TODO: 在删除cache之后，其实本身存在这很大的逻辑漏洞，即，写入失败怎么办，我在这里只是简单的抛出了异常，但是还是删除了Analysis cache文件，这肯定是不对的，但是感觉具体还是太复杂了，短时间没有想出来一个比较合适的方法
    def __createCacheFile(self, name, content):
        dirPath = '../Data/Cache/NLPCache/' + self.__target + '/'
        filePath = dirPath + name
        try:
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            cacheFile = open(filePath, 'a+')
            cacheFile.write(json.dumps(content))
            os.remove(self.__regularizedCachePath +name)
        except IOError as err:
            print "Error is " + str(err)
            print "Error in Creating or writing into Data/Cache/NLPCache" + self.__target + '/' + name
        finally:
            if 'cacheFile' in locals():
                cacheFile.close()



test = nlp('RT22z3DL.13450.vPiFD1J5MM6r', "中南大学", 0, poolSize=5, timer=1000)