 #coding=utf-8
import urllib.request
import threading
import re
import os
import sys
import socket
import _database_ as DB
import pymysql

socket.setdefaulttimeout(60)
GV_DOWNLOAD_ALL = []
GV_THEAD_COUNT = 4   #并发下载线程数
GV_FINISHED_COUNT = []
GV_POCESSSUM = []
GV_TIEBANAME = ""
page = 0
x=0
max_page = 0
DBCONN = pymysql.connect(host=DB.DBL_CONNECTION_HOST, port=3306,user=DB.DBL_CONNECTION_USER,passwd=DB.DBL_CONNECTION_PASSWORLD,db=DB.DBL_CONNECTION_DATABASE_NAME,charset='UTF8')
DBCONN.set_charset('utf8mb4')
DBCUR = DBCONN.cursor()
DBCUR.execute("SET names 'utf8mb4'")
print("数据库初始化完毕")


GV_ERROR_THREAD_DATA = []   #该变量用来储存出错线程数据，包括线程编号，当前线程下载位置，线程目标下载位置（里面储存的是list，按照该顺序排列）

#该函数用来下载网页，如果出错会一直循环下载
#返回值：网页源代码
def getHtml(url):
    while True:
        try:
            page = urllib.request.urlopen(url,timeout=5)
            html = page.read()
            return html
        except Exception as e:
            print("下载出错！重试中...",end="\t")
            pass

#该函数用来匹配出网页中的所有帖子以及相应的帖子链接
#返回值：匹配的帖子数量，帖子数据
def getTitle(html):
    #    <a href="/p/4745088342" title="DDD" target="_blank" class="j_th_tit ">DDDD</a>
    reg = r"<a href=\"/p/.*?class=\"j_th_tit \">.*?</a>"
    imgre = re.compile(reg)
    titlelist = re.findall(imgre,html)
    t=1
    sum = len(titlelist)
    dstr = '\r\n\t\t'
    author = ""
    date = ""
    replydata = ""
    for dta in titlelist:
        #匹配帖子标题
        nextpage = ""
        psum = 0
        firstfloor = True
        print("#",end="")
        sys.stdout.flush()
        k = re.sub("<a href=\"/p/.*?class=\"j_th_tit \">","",dta)
        k = re.sub("</a>","",k)
        #匹配帖子地址,用来获得作者和发帖时间
        postUrl = re.sub("<a href=\"","",dta)
        postUrl = re.sub("\" title=.*?class=\"j_th_tit \">.*?</a>","",postUrl)
        fatherurl = postUrl
        author = ""
        while nextpage != "NULL": #抓取一个帖子的所有页面
            psum , author , nextpage= getPostPages(postUrl,fatherurl,author)
            postUrl = nextpage
            if firstfloor == True:
                firstfloor = False
            t+=psum
        t += 1
        print("-",end="")
        DB_COMMIT()
        print("=",end="")
    print("\n")
    GV_FINISHED_COUNT[0] += 1
    return t,dstr

#得到帖子的第一页所有回帖，作者以及回帖时间
#返回值：作者，发帖时间，回复数据
def getPostPages(suburl,fatherurl,postauthor):
    html = getHtml('http://tieba.baidu.com' + suburl)
    html = html.decode('utf-8','ignore')
    #首先寻找是否有下一页
    NEXT_PAGE = ">下一页</a>" 
    nextpage_pos = html.find(NEXT_PAGE)
    nextpage = html[nextpage_pos-29:nextpage_pos-1]
    nextpage = nextpage[nextpage.find("\"")+1:]
    if nextpage_pos == -1:
        nextpage = "NULL"
    #print("nextpage_pos=",nextpage_pos,nextpage)
    #os.system("pause")
    postDate = ""
    postAuthor = ""
    reply = ""
    if postauthor == "":
        #寻找用户名
        head = "author:"
        tail = "thread_id"
        start = html.find(head)
        end = html.find(tail,start)
        postAuthor = html[start+len(head):end]
        postAuthor = cleanhtml(postAuthor)
        postAuthor = clearNonEssential(postAuthor)
        #寻找回帖
        head = " j_d_post_content"
        tail = "<div class=\"user-hide-post-down\" style=\"display: none;\">"
        start = html.find(head)
        end = html.find(tail,start)
        reply = html[start+len(head):end]
        html = html[end+len(tail):]
        reply = cleanhtml(reply)
        reply = clearNonEssential(reply)
        #寻找时间
        head = "&quot;date&quot;:&quot;"
        tail = "&quot;,&quot;vote_crypt&quot;:&quot;&quot;,&quot;post_no&quot;"
        postdate_head_typeB = "楼</span><span class=\"tail-info\">"
        postdate_tail_typeB = "</span></div><ul class=\"p_props_tail props_appraise_wrap\">"
        start = html.find(head)
        end = html.find(tail,start)
        postDate = ""
        if end < 0 or start < 0 :
            #在寻找时间的时候没有找到，说明采用了typeB
            start = html.find(postdate_head_typeB)
            end = html.find(postdate_tail_typeB)
            if end < 0 or start < 0 :
                print("-NMTERR-",end="")
                postDate = "1996-10-30 22:58"
            date = html[start+len(postdate_head_typeB):end]
            html = html[end+len(postdate_tail_typeB):]
        else:
            postDate = html[start+len(head):end]
            html = html[end+len(tail):]
        postDate = cleanhtml(postDate)
        postDate = timeFormater(postDate)
        postauthor = postAuthor
    replydata = ""
    #print("NOT IN WHILE:postAuthor=",postAuthor,"\tpostDate=",postDate,"\treply=",reply)
    #replydata = replydata + reply + "*#*" + postAuthor + "*#*" + postDate +"$#$"
    #上面的代码完成了1楼信息的抓取
    #接下来寻找第一页的回帖内容================================
    #这个循环用来从当前HTML中匹配出所有用户块
    BLOCK_START_END = "<a style=\"\" target=\"_blank\" class=\"p_author_face \" href=\""
    poblock = []
    while True:
        ibsea = html.find(BLOCK_START_END)
        ibseb = html.find(BLOCK_START_END,ibsea+len(BLOCK_START_END))
        if ibsea < 0 or ibseb < 0:
            break
        userblock = html[ibsea+len(BLOCK_START_END):ibseb]
        poblock.append(userblock)
        html = html[ibseb+len(BLOCK_START_END):]
    print(len(poblock),end="")
    if len(poblock) == 0:
        postDate = "1996-10-30 22:58"
    #os.system("pause")
    #下面这个循环用来从所有用户块中匹配出发帖时间，帖子内容，作者信息
    #寻找该页的所有回帖内容
    head = " j_d_post_content"
    tail = "<div class=\"user-hide-post-down\" style=\"display: none;\">"
    #寻找发帖用户
    username_head="<img username=\""
    username_tail="\" class=\"\" src=\""
    #寻找发帖时间  ***由于百度贴吧太老，所以有2种时间匹配方式
    postdate_head="&quot;date&quot;:&quot;"
    postdate_tail="&quot;,&quot;vote_crypt&quot;:&quot;&quot;,&quot;post_no&quot;"
    postdate_head_typeB = "楼</span><span class=\"tail-info\">"
    postdate_tail_typeB = "</span></div><ul class=\"p_props_tail props_appraise_wrap\">"
    first = True
    psum = 0
    for html in poblock:
        #寻找作者
        start = html.find(username_head)
        end = html.find(username_tail)
        if end < 0 or start < 0 :
            break
        author = html[start+len(username_head):end]
        html = html[end+len(username_tail):]
        author = cleanhtml(author)
        author = clearNonEssential(author)
        #寻找回帖内容
        start = html.find(head)
        end = html.find(tail,start+len(head))
        if end < 0 or start < 0 :
            break
        reply = html[start+len(head):end]
        html = html[end+len(tail):]
        reply = cleanhtml(reply)
        reply = clearNonEssential(reply)
        #找到了一个回复，接下来寻找作者和发帖时间
        #寻找发帖时间
        start = html.find(postdate_head)
        end = html.find(postdate_tail)
        if end < 0 or start < 0 :
            #在寻找时间的时候没有找到，说明采用了typeB
            start = html.find(postdate_head_typeB)
            end = html.find(postdate_tail_typeB)
            if end < 0 or start < 0 :
                print("-NMTERR-")
                break
            date = html[start+len(postdate_head_typeB):end]
            html = html[end+len(postdate_tail_typeB):]
        else:
            date = html[start+len(postdate_head):end]
            html = html[end+len(postdate_tail):]
        date = timeFormater(date)
        date = cleanhtml(date)
        if first == True:
            postDate = date
            first = False
        #os.system("pause")
        psum+=1   
        reply = reply.replace("\"","")
        DB_Insert(fatherurl,GV_TIEBANAME,author,reply,date,postauthor,suburl)  
    #返回结果
    return psum , postAuthor  , nextpage

#下面的函数用来格式化时间字段，避免数据分析模块出错
def timeFormater(timestr):
    ss = timestr.replace(" ","")
    if len(timestr) < 8:
        ss = "1996-10-30 22:58"
    elif timestr[10] != " ":
        ss = timestr[:9] + " " + timestr[10:]
    else:
        ss = timestr
    return ss

#清除不必要信息
def clearNonEssential(strd):
    nonesslist = [">","\""," ",",","\n","\r","clearfix"]
    dstr = strd
    for item in nonesslist:
        dstr = dstr.replace(item,"")
    return dstr
#该函数用来去掉回帖中无关HTML标签，只保留中文/英文
#返回值：无HTML标签的回帖数据，如果出错，返回空字符串
def cleanhtml(reply):
  cleanr = re.compile('<.*?>')
  onlytext = re.sub(cleanr, '', reply)
  return onlytext



#该函数用来下载网页，为【入口函数】，以上所有函数均由该函数直接/间接调用
def downloadPage(psum,count,begURL,beg=0):
    GV_POCESSSUM.append((psum-beg)*GV_THEAD_COUNT)
    x=beg
    page = x*50
    GV_DOWNLOAD_ALL.append(False)
    errored = False
    while x < psum and errored == False:
        try:
            print('>>>>>线程 '+str(count)+'：当前正在下载第【',str(x + 1)+'/'+str(psum),'】页数据')
            html = getHtml(begURL + str(page))
            #pocessList.append(html)
            saveToFile(html,count,x+1) #为了减小内存暂用，我们将其放入文件
        except Exception:
            print('>>错误->线程 '+str(count)+'：在下载第【',str(x + 1)+'/'+str(psum),'】页数据时出错！程序将会重试。*****下载出错。')
            GV_ERROR_THREAD_DATA.append([count,x,psum])   #返回出错页面和下载总数
            errored = True
        x += 1
        page +=50
    if errored == False:
        print('【线程'+str(count)+'】<<<<<页面全部下载完成！')
        GV_DOWNLOAD_ALL[count-1] = True
    else:
        axa = GV_ERROR_THREAD_DATA[ len( GV_ERROR_THREAD_DATA ) - 1 ]


#该函数用来处理网页的HTML信息，为【第二入口】函数，控制线程的结束与终止
def pocessDataList(GV_COUNT,begURL,tieba_name):
    titlesum = 0
    titlelist = ''
    count = 0
    dstr = '0x0'
    m = 0
    x = 0
    NO_OUT = True
    exit_sum = 0
    GV_TIEBANAME = tieba_name
    dlcachepath  = ".//dlcache//"
    while NO_OUT: 
        htmldata = readSavedHTML()
        if( htmldata != "ERROR" ) :
            count += 1
            print('>>>>>当前正在处理第【',count,'】页的帖子,已抓取',titlesum,'条数据.....',end=' ')
            m , dstr= getTitle(htmldata.decode('utf-8','ignore'))
            titlelist += dstr
            titlesum += m
            x = 0
            for item in GV_DOWNLOAD_ALL:
                if item == True:
                    x += 1
            print('下载完毕！','调试：x=',x,'GV_COUNT=',GV_COUNT)
        flist = os.listdir(dlcachepath)
        #if GV_FINISHED_COUNT[0] == GV_POCESSSUM[0]:
        if len(flist) == 0 and x == len(GV_DOWNLOAD_ALL):
            NO_OUT = False
            break
        #检测是否有线程异常，如果异常，则重新启动
        if len(GV_ERROR_THREAD_DATA) !=0:
            for item in GV_ERROR_THREAD_DATA:
                print('>>尝试重新启动线程 '+str(item[0])+'中.....')
                tn = threading.Thread(target=downloadPage,args=(item[2],item[0],begURL,item[1],))
                print('>>线程 '+str(item[0])+'重新启动完成！')
                tn.setDaemon(True)
                tn.start()
                del GV_ERROR_THREAD_DATA[0]
    DB_clear()
    return titlesum,titlelist


#以下2个函数的目地是为了减少程序的内存占用。
#该函数用来从文件中读取已经下载的HTML数据，然后在将其清空。
def readSavedHTML():
    dlcachepath  = ".//dlcache//"
    flist = os.listdir(dlcachepath)
    if len(flist) == 0:
        return "ERROR"
    f = open(dlcachepath+flist[0],"rb")
    htmldata = f.read()
    f.close()
    delfilecmd = "rm .//dlcache//" + flist[0]
    os.system(delfilecmd)
    return htmldata
#该函数用于将下载的HTML数据写入文件
def saveToFile(htmldata,threadcount,fnum):
    filename = ".//dlcache//" + str(threadcount) + "-" + str(fnum)
    f = open(filename,"wb")
    f.write(htmldata)
    f.close()



#该函数用于将数据插入数据库
def DB_Insert(POSTOF,TIEBANAME,AUTHOR,CONTENT,DATE,REPLYTO,LINK):
    INS = "INSERT INTO `testdb`(`POSTOF`, `TIEBANAME`, `AUTHOR`, `CONTENT`, `DATE`, `REPLYTO`, `LINK`) VALUES ("
    #INS = "INSERT INTO `postdata`(`POSTOF`, `TIEBANAME`, `AUTHOR`, `CONTENT`, `DATE`, `REPLYTO`, `LINK`) VALUES ("
    INS+= "\"" + POSTOF + "\",\"" + TIEBANAME +"\",\"" + AUTHOR + "\",\"" + CONTENT +"\",\"" + DATE +"\",\""+ REPLYTO + "\",\"" + LINK + "\")"
    #print(INS)
    try:
        DBCUR.execute(INS)
    except Exception as e:
        print("SQL-SYNTAX-ERROR",end="")
        return False 
    return True

#提交数据更新
def DB_COMMIT():
    DBCONN.commit()

#该函数用与从数据库中查询
def DB_SELECT():
    INS = "select  NAME from `tr_teacherlist`    where NAME like('%" + word +"%')"
    pass

#该函数用于检查当前数据是否存在于数据库中
def DB_UniqueCheck(postContent,author,date):
    SEL = "select  AUTHOR,DATE from `postdata`    where CONTENT0=\"" + postContent + "\""
    print("查重....")
    DBCUR.execute(SEL)
    DBCONN.commit()
    data = DBCUR.fetchall()
    if(data[0][0] == author and date == data[0][1]):
        return False
    return True

def DB_clear():
    DBCONN.close()


#下面的函数用于子处理函数的多线程模型
def dispatchPocess():
    pass