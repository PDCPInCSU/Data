# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import json
import re
class TiebaContentAnalysis:

    def __init__(self, owner, target):
        self.__owner = owner
        self.__target = target
        content= self.__readCacheFile('5206927219') # 调试ReadCacheFile用
        self.__content = dict()
        self.__getFileAnalyzed(content, '5206927219')

    # 读取文件，但是如果打开文件失败会返回None
    def __readCacheFile(self, name):
        dirPath = '../../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'+self.__target+'/'
        filePath = dirPath + name
        result = None
        # print filePath # 调试用
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

    # TODO: 在删除cache之后，其实本身存在这很大的逻辑漏洞，即，写入失败怎么办，我在这里只是简单的抛出了异常，但是还是删除了Analysis cache文件，这肯定是不对的，但是感觉具体还是太复杂了，短时间没有想出来一个比较合适的方法
    def __createCacheFile(self, name, content):
        dirPath = '../../Data/Cache/SpiderCache/TiebaCache/Regularized Cache/' + self.__target + '/'
        filePath = dirPath + name
        try:
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            cacheFile = open(filePath, 'a+')
            cacheFile.writelines(content)
            os.remove('../../Data/Cache/SpiderCache/TiebaCache/Analysing Cache/'+self.__target+'/'+name)
        except IOError as err:
            print "Error is " + str(err)
            print "Error in Creating or writing into Data/Cache/SpiderCache/TiebaCache/Regularized Cache/" + self.__target + '/' + name
        finally:
            if 'cacheFile' in locals():
                cacheFile.close()
    # 控制整个的进程
    # def __analysingController(self, target, timer, numRange):

    # 对Cache文件进行处理,处理完最后将删除此Cache文件
    # def __contentRegularing(self, content):


    def __getFileAnalyzed(self, content, name):
        contents = dict()
        # 首先将文件里边若干页分离开，便于后边去
        pattern =re.compile(r"<!DOCTYPE html>[\w\W]*?</html>")
        result = re.findall(pattern, content)
        # 然后针对每一个页面去做分段解析
        for eachPage in result:
            contents.update(self.__getSegmented(eachPage))
        self.__createCacheFile(name, str(contents))



    # 将每一个页面的内容按照楼层分割
    def __getSegmented(self, content):
        # print content
        soup = BeautifulSoup(content, 'html5lib')
        content = soup.find_all("div", attrs={'class':["l_post", "j_l_post", "l_post_bright"]})
        # print content[0]
        # TODO：需要在回调的函数里边处理一下为self.__content空的情况
        result = dict()
        for eachContent in content:
            result.update(self.__getSegmentAnalyzed(str(eachContent)))
        # print len(content)
        return result



    # 分析每一层楼的内容，并汇总返回
    def __getSegmentAnalyzed(self, content):
        soup = BeautifulSoup(content, 'lxml')
        # soup = BeautifulSoup(content,convertEntities = BeautifulSoup.HTML_ENTITIES)
        # 然后是content
        content = soup.find("div", attrs={"class":["d_post_content", "j_d_post_content"]}).get_text()
        data_filed =  soup.find("div", attrs={"class":["l_post", "j_l_post",  "l_post_bright"]}).div.parent["data-field"]
        data_filed = json.loads(data_filed)
        # 构造一个字典
        result = {
                        # 用楼层做Key
                        data_filed["content"]["post_no"]:
                        {
                            # 楼主相关信息
                            'Author':
                                    {
                                        'authorId': data_filed["author"]["user_id"],
                                        'authorName': data_filed["author"]["user_name"],
                                        'authorSex': data_filed["author"]["user_sex"]
                                    },
                            # 楼数
                            'Floor': data_filed["content"]["post_no"],
                            # 设备种类
                            'Device': data_filed["content"]["open_type"],
                            # 发言时间
                            'Date': data_filed["content"]["date"],
                            # 发言内容
                            'Content': content
                        }

                    }
        return result



test = TiebaContentAnalysis(0, '刀剑神域')
