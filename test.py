# import os
# root = os.getcwd()
#
# def te(file):
#     path=os.getcwd()+"/Template/"
#     name=path+file
#     file = open(name, 'r', encoding='UTF-8')
#
#     print(file)
#
# te("user.txt")


from jira import JIRA
import logging
import logging.config

# logging.config.fileConfig('logging.conf')
# logger = logging.getLogger('simpleFormatter')
# m=["df"]
# import os
# with open(os.getcwd() + '/Template/' + 'recevers.txt', 'r') as f:
#     recevers = f.read().splitlines()

jira = JIRA(basic_auth=('xiaomenghong@creditease.cn', 'meng12..'),
                  options={'server': 'http://jira.creditease.corp/'})
print(jira)

# jira_caifu = JIRA("http://10.143.143.167:18085/", basic_auth=('admin', 'fso2016'))
# projects=jira_caifu.projects()
#
# print(projects)

# try:
#     assignee = jira.issue('CFDHTFW-1170').fields.assignee.displayName
#     assignee = assignee.replace(" ", "")
# except:
#     logger.warning("缺陷" + str(112) + "经办人错误")
#
# if str(assignee) in m :
#     print("dfdf")