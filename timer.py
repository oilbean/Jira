# coding:utf8
import datetime
import time
import os
import sys
import jira_3


def doSth(time):
    # 程序放在这个类里
    os.system("jira_3.py")
    print(str(time)+u'这个程序要开始疯狂的运转啦')



# 每天下午18:10启动
def main(h=15, m=13):
    
    holiday=[25,26,27]
    
    while True:
        
        now = datetime.datetime.now()
        
        if now.month==10 or now.month ==6:
            if now.day in holiday:
                print("假期")
            else :
                if now.hour == h and now.minute == m:
                    doSth(now)
        else:
            if now.hour == h and now.minute == m:
                doSth(now)
            
        # 每隔60秒检测一次
        time.sleep(60)


main(18,10)
