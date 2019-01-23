#encoding=utf-8
'''
Created on 2018-12-13

@author: zhangxiao2000@gmail.com

This is a configure file, you should set website and the period of education.
这是一个配置文件，配置填表网址和培训起始时间等

'''
from datetime import datetime

InitData="params.txt"
SaveData="loghistory.csv"

InitURL="http://xxx.xx.xx.xxx/g/***** Your website"
startdate=datetime(2018,3,29) #change to your time
enddate=datetime(2019,3,28)
City = "Chicago"

Timerange={
    'f_am_starttime':(8,8,30,59),
    'f_am_endtime':(12,12,0,10),
    'f_pm_starttime':(13,13,10,40),
    'f_pm_endtime':(18,20,0,59)
    }