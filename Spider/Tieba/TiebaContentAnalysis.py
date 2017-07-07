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
        self.__getFileAnalyzed(content)

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

    # 控制整个的进程
    # def __analysingController(self, target, timer, numRange):

    # 对Cache文件进行处理,处理完最后将删除此Cache文件
    # def __contentRegularing(self, content):


    def __getFileAnalyzed(self, content):
        # 首先将文件里边若干页分离开，便于后边去
        pattern =re.compile(r"<!DOCTYPE html>[\w\W]*?</html>")
        # TODO:这里留下来了一个坑,就是说这样匹配之后，因为result[]里边是str，这就导致了他会转置'字符，导致后边的data_filed后边紧跟的'变成了\'但是在经过Beautiful解析的时候没有去掉这个，反而变成了\\'，直接导致了后边在生成JSON的时候出错,而且还导致了一定数据的丢失
        result = re.findall(pattern, content)
        # print result
        # print type(result)
        # 然后针对每一个页面去做分段解析
        for eachPage in result:
            contents = self.__getSegmented(str(eachPage))
            # 然后将内容加入self.__contents,之所以考虑到在这里加而不是在__getSegmented加，
            # 是因为总感觉那样不优美，可能以后有在这里对函数进行拓展的时候不方便
            # for num in range(0, len(contents)):


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
        result = dict()
        # content =
        soup = BeautifulSoup(content, 'lxml')
        # soup = BeautifulSoup(content,convertEntities = BeautifulSoup.HTML_ENTITIES)
        # 然后是content
        content = soup.find("div", attrs={"class":["d_post_content", "j_d_post_content"]}).get_text()
        data_filed =  soup.find("div", attrs={"class":["l_post", "j_l_post",  "l_post_bright"]}).div.parent["data-field"]
        # 为了解决正则导致的奇怪的情况，具体的原因我在__getFileAnalyzed的TODO里边写了
        # data_filed = data_filed[2:]+"\"}}"
        data_filed = json.loads(data_filed)

        # print data_filed
        # 接着是JSON里边的相关信息r
        # data_filed = json.loads(soup.find("div", attrs={"class":["l_post", "j_l_post",  "l_post_bright"]}).div.parent["data-field"])
        # print data_filed
        # 构造一个字典
        contents = {
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
        print contents
        # contents = {}
        return contents



test = TiebaContentAnalysis(0, '刀剑神域')
