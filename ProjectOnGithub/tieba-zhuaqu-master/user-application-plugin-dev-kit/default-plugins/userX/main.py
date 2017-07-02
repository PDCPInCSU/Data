from tkinter import *           # 导入 Tkinter 库
import tkinter.ttk as ttk
import userX
root = Tk()                  
root.resizable(False,False)
root.title("贴吧用户分析")

#KCC基本分析组件
#该组件用于统计特定用户的信息
##插件信息定义
KCC_PLUGIN_NAME="userX"
KCC_PLUGIN_DESCRIPTION="分析某位用户的发帖量，语句关键词"
KCC_PLUGIN_COPYRIGHT="kanch"
##定义结束

def btnclick():
    root.update()
    authorname = wordentry.get()
    SCALE = daysentry.get()
    scaletype = datascaleelem.get()
    print("authorname=",authorname,"\tSCALE=",SCALE,",\tscale type=",scaletype)
    if scaletype == "显示用户关系链（开发中）":
        pass
    elif scaletype == "显示活跃度":
        userX.showLastDays(authorname,int(SCALE))
    elif scaletype == "显示语句关键词":
        userX.showKeyWord(authorname,int(SCALE))
    elif scaletype == "活跃时间段分析":
        userX.activeTimeAnaylize(authorname,int(SCALE))
    else:
        print("出现未知错误：无法正常选择处理类型！")

def centerWindow(rt):
    rt.update() # update window ,must do
    curWidth = rt.winfo_reqwidth() # get current width
    curHeight = rt.winfo_height() # get current height
    scnWidth,scnHeight = rt.maxsize() # get screen width and height
    # now generate configuration information
    tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,
    (scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
    rt.geometry(tmpcnf)
    return rt
    
data = StringVar(root)
scale = IntVar(root)
Label(root,text="KCC数据分析模块 - 基本分析套件\n该模块用于显示指定词语的时间频率关系图",width=35,height=5).pack()
Label(root,text="请输入要分析的用户的ID:",width=25,height=2).pack()
wordentry = Entry(root,text="   ID",width=25,textvariable=data)
wordentry.pack(ipadx=4,ipady=4)
Label(root,text="分析类型:",width=25,height=2).pack()
variable = StringVar(root)
datascaleelem = ttk.Combobox(root, textvariable=variable, values=["天", "月", "年"],state='readonly')
datascaleelem["values"] = ("显示用户关系链（开发中）", "显示活跃度", "显示语句关键词","活跃时间段分析")  
datascaleelem.current(1)  
datascaleelem.pack()
Label(root,text="要统计最近多少天的数据(<=0->all):",width=25,height=2).pack()
daysentry = Entry(root,text="请输统计最近多少天的",width=25,relief=GROOVE,textvariable=scale)
daysentry.pack(ipadx=4,ipady=4)
Button(root, text="显示结果", width=15,relief=GROOVE,command=btnclick).pack(pady=16,ipadx=8,ipady=8)

root = centerWindow(root)
root.mainloop()                 # 进入消息循环
