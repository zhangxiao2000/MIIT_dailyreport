#encoding=utf-8
'''
Created on 2018-4-25

@author: zhangxiao2000@gmail.com

This script read daily report content from params.txt and daily\daily_yyyymmdd.txt
You can run this first to check if all data are correct before filling to the website.

这个脚本从params.txt和daily\daily_yyyymmdd.txt中读取数据
可以先单独运行这个脚本检查要填写的数据是否正确

'''
import os
from datetime import datetime
import time
import random
from setting import InitData, SaveData

def readdata(fname):
    d={}
    f=open(fname)
    while True:
        line = f.readline()
        if not line:
            break
        if line.startswith('#'):
            continue
                
        l=line.split(':')
        if len(l)>1: # it has key and value
            key=l[0].strip()
            value=':'.join(l[1:])
            value=value.strip()
            d[key]=value
        #Str Process
    f.close()
    
    return d
    

def preparedata(suffix,fname=InitData):
    detail={}
    #Basic data from params.txt
    #从params.txt中读取基础数据
    d=readdata(fname)
    getrandomtime(d)
    detail.update(d)
    
    detail['status']="basic"

    #Different data from daily\daily_yyyymmdd.txt
    #从daily\daily_yyyymmdd.txt中读取每天不同的数据    
    dailyname="daily\\daily_{}.txt".format(suffix)
    if os.path.exists(dailyname):
        d=readdata(dailyname)
        if (len(d.keys())>0):
            detail.update(d)
            detail['status']="finished"
    else:
        dayOfWeek = datetime.now().weekday()   
        if dayOfWeek==6: #Saturday for rest
            return None
  
    return detail    

def printdata(data):
    for k,v in data.items():
        print("{:<20}:{}".format(k,v))

def savedata(suffix,data):
    if not os.path.exists(SaveData):
        d=readdata(InitData)
        title="Date,"
        for k in d.keys():
            if k!="status":
                title=title+"{},".format(k)
        
        title=title+",status\n"
        f=open(SaveData,"w")
        f.write(title)
        f.close()
        
    
    s="{},".format(suffix)
    for k in data.keys():
        if k!="status":
            s=s+'"{}",'.format(data[k])
    
    s="{},{}\n".format(s,data['status'])
    
    #print(data['status']=="finished",data['status']=="basic")

    f=open(SaveData,"a+")
    print(s)
    f.write(s)
    f.close()

def getdata(delta=0):
    #dayOfWeek = datetime.now().weekday()
    #dstr=time.strftime("%Y/%m/%d",time.localtime(time.time()))
    suffix=time.strftime("%Y%m%d",time.localtime(time.time()+delta))
    d=preparedata(suffix)
    if d==None:
        print(suffix," for rest.")
    else:
        print(suffix,".data status:",d['status'])
    
    return d
    
def gettodaydata():
    return getdata(0)
    
def getyesterdaydata():
    #24*60*60=86400 seconds to get yesterday date.
    return getdata(-86400)

def gettime(starthour,endhour,startminite,endminite):
    h=random.randint(starthour,endhour)
    m=random.randint(startminite,endminite)
    s="%02d:%02d"%(h,m)
    return s
    
def get_f_am_starttime():
    return gettime(8,8,30,59)

def get_f_am_endtime():
    return gettime(12,12,0,10)

def get_f_pm_starttime():
    return gettime(13,13,10,40)

def get_f_pm_endtime():
    return gettime(18,20,0,59)

def getrandomtime(data):
    #如果每天培训时间范围基本固定，可以修改随机时间范围，简化填表过程
    #如果每天时间固定，则把时间范围固定即可
    if  not isinstance(data, dict):
        return None
    
    items=['f_am_starttime','f_am_endtime','f_pm_starttime','f_pm_endtime']
    for i in items:
        if i in data.keys():
            funcname="get_"+i
            data[i]=eval(funcname)()
        
    return data 

if __name__ == '__main__':
    data=gettodaydata()
    print()
    printdata(data)
