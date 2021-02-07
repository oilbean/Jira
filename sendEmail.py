#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import datetime
import logging
import logging.config
import os


def send_email(file_name,recevers,email_name):


    today = datetime.date.today()
    
    receivers = recevers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEMultipart('alternative')

    emailPath=os.getcwd()+"/Template/Email/"
    excelPath=os.getcwd()+"/ExcelData/"

    f=open(emailPath+email_name,'rb')
    mail_msg = f.read()
    f.close()

    message['From'] = Header("测试环境_BUG统计预警", 'utf-8')
    message['To'] = Header("财富研发部", 'utf-8')

    subject = ' 质量监控日报-财富研发部（'+str(today)+')'
    message['Subject'] = Header(subject, 'utf-8')

    part1=MIMEText(mail_msg,'html','utf-8')

    # 构造附件2，传送当前目录下的 runoob.txt 文件
    att2 = MIMEText(open(excelPath+file_name+'.xls', 'rb').read(),'plain', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = "'attachment',filename=('gbk','bug.xls')'"
    att2.add_header('Content-Disposition', 'attachment', filename=('gbk', '', file_name+".xls"))

    message.attach(att2)
    message.attach(part1)

    for i in range(len(receivers)):
        
        try:
            smtpObj = smtplib.SMTP('')
            
            sender = ''
            password=""

            login_result = smtpObj.login(sender, password)
            print(login_result)

            smtpObj.sendmail(sender, receivers[i], message.as_string())
            print("邮件发送成功")
            
            logging.info(str(receivers[i])+"邮件发送成功")
            
        except smtplib.SMTPException:
            print("邮件发送失败")
            logging.info(str(receivers[i])+"Error: 无法发送邮件")
