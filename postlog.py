#encoding=utf-8
'''
Created on 2018-4-3

@author: zhangxiao2000@gmail.com

Run this script to auto fill the daily report
使用这个脚本自动填写日志
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
from dailydata import *
from setting import SaveData,InitURL,startdate,enddate,City

driver=webdriver.Firefox(executable_path="geckodriver")


def commonprepare(url,yesterday=False):
    driver.get(url)
    
    assert '外专局境外监管系统' in driver.title
    
    #https://blog.csdn.net/xiaodanpeng/article/details/50999026
    # 鼠标输入事件
    driver.find_element_by_id("addrecord").click()
    
    #第二页
    if yesterday:
        driver.find_element_by_id("yesterdayLog").click()
        
    pos=driver.find_element_by_id("f_visicity")
    if pos.get_attribute("value")=="":
        pos.send_keys(City)
    # 鼠标输入事件
    driver.find_element_by_id("study").click()    
    
    return driver
    
def postcontent(frame_id,content):
#http://yizeng.me/2014/01/31/test-wysiwyg-editors-using-selenium-webdriver/#heading-tinymce-4015     
    #post data in a tinymce rich text box    
    tinymce_frame =driver.find_element_by_id(frame_id)
    driver.switch_to.frame(tinymce_frame)
    tinymce_body = driver.find_element_by_id("tinymce")
    #"Read paper:Challenges of workload analysis on large HPC systems; A case study on NCSA Bluewaters"
#    if len(tinymce_body.get_property("value"))>0:
    tinymce_body.clear()
    content=content.replace("**",u'\ue007')
    tinymce_body.send_keys(content)
    driver.switch_to.default_content()
    
def getcontent(frame_id):
#http://yizeng.me/2014/01/31/test-wysiwyg-editors-using-selenium-webdriver/#heading-tinymce-4015     
    #post data in a tinymce rich text box    
    tinymce_frame =driver.find_element_by_id(frame_id)
    driver.switch_to.frame(tinymce_frame)
    tinymce_body = driver.find_element_by_id("tinymce")
    #"Read paper:Challenges of workload analysis on large HPC systems; A case study on NCSA Bluewaters"
#    if len(tinymce_body.get_property("value"))>0:
    #value = tinymce_body.get_attribute("value")
    tinymce_txt=driver.find_element_by_tag_name("body")
    print(tinymce_txt)
    print(tinymce_txt.get_attribute("text"))
    print(tinymce_txt.get_attribute("value"))
    print("value",tinymce_body.get_attribute("value"))
    print("value2",tinymce_body.get_attribute("Value"))    
    print("text",tinymce_body.get_attribute("body"))
    print("text",tinymce_body.get_property("body"))
    print("text",tinymce_body.get_attribute("f_am_content"))    
    driver.switch_to.default_content()     
    
    print(tinymce_body)
    return tinymce_body 
   
def postlog(url,yesterday=False):
    
    driver =commonprepare(url,yesterday)
    if yesterday:
        d=getyesterdaydata()
    else:
        d=gettodaydata()
    #d['f_log_date']=dstr
    
    if d==None:
        havearest(driver)
        return 0
    
    for k in d.keys():
        if k=="status":
            pass
        elif k=="f_am_content":
            postcontent("f_am_content_ifr",d[k])
        elif k=="f_pm_content":
            postcontent("f_pm_content_ifr",d[k])
        else:
            input_form=driver.find_element_by_name(k)
            input_form.clear()
            input_form.send_keys(d[k])
 
    print(d['status'])
    now = datetime.now()
    timestr=now.strftime('%Y.%m.%d-%H:%M:%S') 
    
    #https://www.cnblogs.com/mengyu/p/6952774.html does not work
    #nb=driver.find_element_by_name(u"确定")
    #cb=driver.find_element_by_class_name("btn btn-default")

    if (now.hour<18 or d['status']!='finished' and now.hour<21) and (yesterday==False):
        driver.find_element_by_id("save_btn").click()
        time.sleep(5)
        #xpath for 确定
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div/div/div[4]/button").click()
        time.sleep(20)
        print(timestr,"basic state, just save it.\n")
    else:
        #Check your data in 40 seconds, if something is wrong, modify it online or close the browser.
        #等待40秒，如在此时间内发现填表错误，可手工修改或关闭浏览器更正后再次运行
        
        time.sleep(40)
        driver.find_element_by_id("submit_btn").click()        
        #xpath for 确定
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div/div/div[4]/button[1]").click()
        print("{}: status:{}. \n".format(timestr,d['status']))    
        savedata(timestr,d)
    
def getlog(url):   
     
    f=open(SaveData,"a+")
    
    driver =commonprepare(url)    
    date=driver.find_element_by_id("f_current_date").get_property("value")
    print(date)
    am_record="{},AM,".format(date)
    pm_record="{},PM,".format(date)

    d=preparedata()    
    
    
    for k in d.keys():
        if k=="f_am_content":
            #postcontent("f_am_content_ifr",d[k])
            value=getcontent("f_am_content_ifr")
        elif k=="f_pm_content":
            value=getcontent("f_pm_content_ifr")
            pass
        else:
            input_form=driver.find_element_by_name(k)
            value=input_form.get_property("value")
            print(value)
            
        if k.startswith("f_am"):
            am_record+='"{}",'.format(value)
        else:
            pm_record+='"{}",'.format(value)
                
    print(am_record)
    print(pm_record)
    f.write(am_record)
    f.write("\n")
    f.write(pm_record)
    f.write("\n")
    
    f.close()

def havearest(url):
    
    dayOfWeek = datetime.now().weekday()
   
    if dayOfWeek==5 or dayOfWeek==6: #Sunday and Saturday
        driver.find_element_by_id("onwayrecord").click()
        driver.find_element_by_id("rest_submit_btn").click()
        time.sleep(40)
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div/div/div[4]/button[1]").click()

    return

if __name__ == '__main__':    
    now = datetime.now()
    
    if now>startdate and now<enddate:
        #postlog(InitURL,True) 填写昨天日志
        postlog(InitURL) #填写当天日志

    else:
        print("Not between the period, please stop the script.\n")
    #getlog(InitURL)
    time.sleep(5)
    driver.close()
    #driver.quit()
    #第一页
 
    
    
    
    
    
    