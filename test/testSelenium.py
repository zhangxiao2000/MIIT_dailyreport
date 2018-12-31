#encoding=utf-8
'''
Created on 2018-12-31

@author: zhangxiao2000@gmail.com

This is a script test if your Selenium environments are ready.
这个脚本测试Selenium环境是否配置正常
'''
from selenium import webdriver
import time
import traceback

def geturl(driver,url="http://www.baidu.com"):
    try:
        ret=driver.get(url)
        time.sleep(10)
        print("Everything is OK, please continue.")
    except :        
        print(traceback.print_exc())
        print("Wrong parameters or wrong Selenium setting.")
        
    finally:
        driver.close()
    
def testFirefox():
    driver=webdriver.Firefox()
    return driver

def testChrome():
    driver = webdriver.Chrome()
    return driver

def testIe():
    driver = webdriver.Ie()
    return driver

    
if __name__ == '__main__':
    driver=testFirefox() #选择你的浏览器，测试能否使用Selenium打开百度首页
    geturl(driver)
    