# MIIT_dailyreport
A program for automatically filling out the daily reports online for overseas persons funded by the Ministry of Industry and Information Technology.


这是一个自动填写工信部出国人员日报的程序，用于简化每日填写日报的工作量。
这个程序在使用前需要根据个人的情况进行修改，所以不适用于没有一点编程基础的人。

工程文件组成及作用
README.md                 这个文件介绍如何使用该工程
setting.py                配置填表网址和培训期间
dailydata.py              这个脚本从两个文件中读取填表所需信息
postlog.py                自动填表脚本
params.txt                每日相同的表格数据
daily\daily_yyyymmdd.txt  每日不同的数据
test\testSelenium.py      测试Selenium环境是否正常的程序

环境准备:
1.安装python和Selenium,参考https://www.jianshu.com/p/52d3ea9c4792
2.运行test\testSelenium.py,如能正常打开baidu首页则可以继续，否则回到1继续准备环境。

使用前:
1.修改setting.py，修改对应的网址，培训起止日期。
2.修改params.txt 修改每日相同的数据，比如培训地点，讲师和联系方式等
3.在daily目录下创建一个daily_yyyymmdd.txt文件，内容可以写上当天的工作内容，注意格式
4.运行dailydata.py查看程序是否可以正确解析并打印工作内容
5.运行postlog.py查看程序是否正确打开了日报填写的网址并填入了对应的内容

日常使用:
1.在daily目录下创建一个daily_yyyymmdd.txt文件，内容可以写上当天的工作内容，注意格式
2.运行postlog.py自动填表
3.自动填表的内容会追加在loghistory.csv中

其他:
如果有什么不便之处，请尽量自行修改。
如果对程序有什么建议，可联系zhangxiao2000@gmail.com。
但是作者不会帮你配置环境。




