import tiebaTitle as TT
import urllib.request
import os
import sys
import time
import threading
import MailService
import pickle
import datetime


#该脚本用来抓取我们贴吧帖子的标题
begURL = 'http://tieba.baidu.com/f?'
#主程序逻辑
TT.setupfiles()
os.system('cls')
print('>>>>>该脚本用来抓取贴吧帖子的标题，可以用作舆情分析\n>>>>>by Kanch kanchisme@gmail.com')
opt = input('\r\n>>>>>是否要指定抓取的贴吧？如果不指定，将会默认抓取【成都信息工程大学】吧。（Y/N）:____\b\b')
if opt == 'Y':
    tieba_name = input('>>>>>请输入要抓取的贴吧：______________________\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')
    print('>>>>>程序将会抓取【' + tieba_name + '】吧！')
else:
    tieba_name = '成都信息工程大学'
    print('>>>>>未指定贴吧，默认抓取【成都信息工程大学】吧！')
KWD = urllib.parse.urlencode({'kw':tieba_name})
begURL = begURL + KWD + '&ie=utf-8&pn='
TT.max_page = input('>>>>>请输入需要抓取的页数：______\b\b\b\b\b')

GTC = input('>>>>>请输入并发线程数量（程序将会使用多线程下载网页，过大易出问题，取决于您的CPU核心数量 2,4,.....）：_____\b\b\b')
TT.GV_THEAD_COUNT = int(GTC)

mstr = "============================================================\r\n抓取结果\r\n============================================================="
createdtime = datetime.datetime.now()
createdtime.strftime('%Y-%m-%d %H:%M:%S')  
#======================================================================================
#=================================主程序逻辑=======================================
#我们用一个线程下载网页，一个线程处理下载后的数据。
#======================================================================================
time1 = time.time()
#下面是多线程方案
MAX_PAGE = int(TT.max_page)
#创建线程
t = []   
x = 0
deltaX = MAX_PAGE / TT.GV_THEAD_COUNT
BEG = 0
END = deltaX
while x < TT.GV_THEAD_COUNT:
    tn = threading.Thread(target=TT.downloadPage,args=(int(END),x+1,begURL,int(BEG),))
    t.append(tn)
    x += 1
    BEG += deltaX
    END += deltaX


#启动线程
for item in t:
    item.setDaemon(True)
    item.start()
#循环处理数据
sum,mstr = TT.pocessDataList(TT.GV_THEAD_COUNT,begURL)
#===================================全部处理完毕，储存至文件======================================
now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')  
last_data_source = {'sum':sum,'time':now}

TT.savetofile(mstr,'C:\\ktieba\\result.txt')
f = open('C:\\ktieba\\result_add','wb')
pickle.dump(last_data_source, f,2)
f.close()
time2 = time.time()
tc = time2 - time1
print('>>>>>抓取完毕！耗时：',str(tc),'秒\n>>>>>共抓取【',sum,'】条数据\n>>>>>结果已经保存至','C:\\ktieba\\result.txt')
#=============邮件提醒===================
#计算耗时
totalseconds = tc
days = int(tc/86400)
tc -= days*86400
hours = int(tc/3600)
tc -= hours*3600
minutes = int(tc/60)
tc -= minutes*60
timscost = str(days) + " days," + str(hours) + " hours," + str(minutes) + " minutes," + str(tc) + " seconds. (total:" + str(totalseconds) + "seconds)"
#邮件正文
Title = "Download Success! Finised on " + str(now) + '.'
line1 = "Tieba job(" + tieba_name +" )created on " + str(createdtime) + " now has been finised!\r\n=========================\r\nSummary\r\n\r\n"
line2 = "\r\nJob Created on: \t"+str(createdtime)+'\r\nJob finished on: \t'+str(now) +"\r\nPieces of data retrived:   " + str(sum) +"\r\nTime cost: \t" + timscost
line3 = "\r\n\r\n\r\n This mail is send by Kanch's PythonBot @ AmazonECS\r\n=========================\r\n"
Content = line1 + line2 + line3
#print(Title,'\r\n',Content)
MailService.SendMail('1075900121@qq.com',Title,Content)