# -*- coding: UTF-8 -*-
from jira import JIRA
import excel
import logging
import logging.config
import datetime
import shutil
import sendEmail
import os

def project(jira):

    dict = {}
    if jira==jira_caifu:

        projects=jira.projects()

        for i in range(len(projects)):
            name=projects[i].name
            key=projects[i].key
            if name =='aaaaaaaa' or name =='项目管理':
               pass
            else:
                m=jira.project_versions(key) #获取项目下所有版本信息

                # 获取版本名称，id，并按id进行排序
                #返回数据格式{'普泽私募': [('双录', '11904'), ('产品列表优化', '11604')]}
                a=[]
                for j in range(len(m)):


                    b = m[j].name
                    c = m[j].id
                    if key == "GP" and b=="1.0.0":
                        pass
                    else:
                        a.append((b, c))
                a.sort(key=takeSecond, reverse=True)

                dict[name]=a

    elif jira==jira_jishu:
        projects=["DTSAFE","FUTURE","GP","CFDHTFW"]
        # projects=['FUTURE']
        for i in range(len(projects)):

            project=jira.project(projects[i])
            name=project.name
            key=project.key

            m = jira.project_versions(key)

            a = []
            for j in range(len(m)):
                b = m[j].name
                c = m[j].id
                if key == "GP" and b == "1.0.0":
                    pass
                else:
                    a.append((b, c))
            a.sort(key=takeSecond, reverse=True)
            dict[name] = a

    logger.info("项目版本"+str(dict))
    return dict

def version_issue(project_name,version,jira):


    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    affectedVersion = ' and affectedVersion = "'
    sign='"'

    if version=="无":
        version=''
        affectedVersion=' and affectedVersion = EMPTY '

        sign=''

    if project_name=="Capital Call":
        project_name='CC'

    #项目-版本 BUG 总数 解决结果为 Unresolved(未解决）、Fixed（已修复）、Incomplete（未完成）、重复提交

    jql_allissue = "project="+project_name+affectedVersion+str(version)+sign+' And resolution in (Unresolved, Fixed, Incomplete, 重复提交) ORDER BY created DESC'
    print(jql_allissue)

    jql_allissue_jishu="project="+project_name+affectedVersion +str(version)+sign+' and issuetype = 缺陷 ORDER BY created DESC'
    print(jql_allissue_jishu)

    #项目-版本 解决结果won't fix
    jql_wontfix = "project="+project_name+affectedVersion+str(version)+sign+' And resolution in ("Won'+"'t Fix"+'") ORDER BY created DESC'
    print(jql_wontfix)

    jql_wontfix_jishu = "project=" + project_name + affectedVersion + str(version) + sign + ' and issuetype = 缺陷 And status in ("无效bug","外部原因","不予解决") ORDER BY created DESC'
    print(jql_wontfix_jishu)

    #项目-版本 今日新建bug
    jql_dayNewissue="project="+project_name+affectedVersion+str(version)+sign+'  and created >='+ str(today)+ " AND created < "+str(tomorrow)
    print(jql_dayNewissue)

    jql_dayNewissue_jishu="project="+project_name+affectedVersion+str(version)+sign+' and issuetype = 缺陷 and created >='+ str(today)+ " AND created < "+str(tomorrow)
    print(jql_dayNewissue_jishu)
    #项目-版本 今日解决bug
    jql_dayReissue="project="+project_name+affectedVersion+str(version)+sign+' and resolved >='+ str(today)+ " AND resolved < "+str(tomorrow)
    print(jql_dayReissue)

    jql_dayReissue_jishu="project="+project_name+affectedVersion+str(version)+sign+' and issuetype = 缺陷 and status changed To 已修复 DURING ("'+str(today)+'","'+str(today)+'")'
    print(jql_dayReissue_jishu)

    # 项目-版本 今日关闭bug
    jql_dayCloissue="project="+project_name+affectedVersion+str(version)+sign+' and status changed To Closed DURING ("'+str(today)+'","'+str(today)+'")'
    print(jql_dayCloissue)

    jql_dayCloissue_jishu = "project=" + project_name + affectedVersion + str(version) + sign + ' and issuetype = 缺陷 and status changed To 已关闭 DURING ("' + str(today) + '","' + str(today) + '")'
    print(jql_dayCloissue_jishu)

    if jira==jira_caifu:
        allissue = jira.search_issues(jql_allissue, maxResults=10)
        all_issue_total = allissue.total

        wontfix = jira.search_issues(jql_wontfix,maxResults=10)
        wontfix_total=wontfix.total

        today_new_issue=jira.search_issues(jql_dayNewissue,maxResults=10)
        today_new_issue_total=today_new_issue.total

        today_resloved_issue = jira.search_issues(jql_dayReissue, maxResults=10)
        today_resloved_total = today_resloved_issue.total


        today_closed_issue = jira.search_issues(jql_dayCloissue, maxResults=10)
        today_closed_issue_total = today_closed_issue.total


    elif jira==jira_jishu:

        if project_name=="财富端后台测试组":
            time = today - datetime.timedelta(days=14)

            jql_allissue_jishu = "project=" + project_name + affectedVersion + str(
                version) + sign + 'and issuetype = 缺陷 and createdDate >= '+str(time)+' ORDER BY created DESC'

            allissue = jira.search_issues(jql_allissue_jishu, maxResults=10)
            all_issue_total = allissue.total

            jql_wontfix_jishu = "project=" + project_name + affectedVersion + str(version) + sign + ' and issuetype = 缺陷 and createdDate >= '+str(time)+' And status in ("无效bug","外部原因","不予解决") ORDER BY created DESC'

            wontfix = jira.search_issues(jql_wontfix_jishu, maxResults=10)
            wontfix_total = wontfix.total

        else:
            allissue = jira.search_issues(jql_allissue_jishu, maxResults=10)
            all_issue_total = allissue.total


            wontfix = jira.search_issues(jql_wontfix_jishu, maxResults=10)
            wontfix_total = wontfix.total

        today_new_issue = jira.search_issues(jql_dayNewissue_jishu, maxResults=10)
        today_new_issue_total = today_new_issue.total

        today_resloved_issue = jira.search_issues(jql_dayReissue_jishu, maxResults=10)
        today_resloved_total = today_resloved_issue.total

        today_closed_issue = jira.search_issues(jql_dayCloissue_jishu, maxResults=10)
        today_closed_issue_total = today_closed_issue.total

    if all_issue_total != 0:
        new_credit = allissue[0]

        new_credit_time = jira.issue(new_credit, fields='created').fields.created

        new_credit_time = new_credit_time[0:10]
        logger.info("获取" + project_name + version + "最新问题创建时间:" + new_credit_time)
    else:
        new_credit_time = "该项目下无缺陷"
    pass


    logger.info("获取" + project_name + "最新问题创建时间:" + new_credit_time)



    return all_issue_total,new_credit_time,today_new_issue_total,today_resloved_total,today_closed_issue_total,wontfix_total

def issue_data(project_name,version,jira):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    affectedVersion = ' and affectedVersion = "'
    sign='"'

    if version=="无":
        affectedVersion = ''
        version=''
        sign=''

    if project_name=="Capital Call":
        project_name='CC'

    #项目-版本 未解决bug
    jql_unResissue="project=" + project_name + affectedVersion + str(version) +sign+ ' AND resolution = Unresolved ORDER BY created DESC'
    print(jql_unResissue)

    jql_unResissue_jishu = "project=" + project_name + affectedVersion + str(version) + sign + ' and issuetype = 缺陷 AND status in(NEW,已确认,Reopen) ORDER BY created DESC'
    print(jql_unResissue_jishu)


    #项目版本 24小时 未解决bug
    jql_unResissue_OT = "project=" + project_name + affectedVersion + str(version) + sign+' and status in (Open, '+"'In Progress') AND created <= -24h or (project=" + project_name + affectedVersion + str(version) + sign+' and status = Reopened AND updated  <= 24h) ORDER BY created DESC'
    print(jql_unResissue_OT)

    jql_unResissue_OT_jishu= "project=" + project_name + affectedVersion + str(version) + sign + ' and issuetype = 缺陷 and status in (NEW,Reopen,已确认'+") AND created <= -24h or (project=" + project_name + affectedVersion + str(version) + sign + ' and status = Reopened AND updated  <= 24h) ORDER BY created DESC'
    print(jql_unResissue_OT_jishu)

    #项目版本 未关闭bug
    jql_Resissue="project=" + project_name + affectedVersion + str(version) + sign+' AND status  = Resolved ORDER BY created DESC'
    print(jql_Resissue)

    jql_Resissue_jishu = "project=" + project_name + affectedVersion + str(version) + sign + ' and issuetype = 缺陷 AND status  in (无法复现,已修复) ORDER BY created DESC'
    print(jql_Resissue_jishu)

    # 项目版本 24小时 未关闭bug
    jql_Resissue_OT = "project=" + project_name + affectedVersion + str(version) + sign+' and status = Resolved AND resolved <= -24h ORDER BY created DESC'
    print(jql_Resissue_OT)

    jql_Resissue_OT_jishu = "project=" + project_name + affectedVersion + str(
        version) + sign + ' and issuetype = 缺陷 and status  in (无法复现,已修复) AND updatedDate <= -24h ORDER BY created DESC'
    print(jql_Resissue_OT_jishu)

    if jira==jira_caifu:

        unRes_issue=jira.search_issues(jql_unResissue,maxResults=10)
        unRes_issue_total=unRes_issue.total

        unRes_issue_OT=jira.search_issues(jql_unResissue_OT,maxResults=10)
        unRes_issue_OT_total=unRes_issue_OT.total

        Resissue=jira.search_issues(jql_Resissue,maxResults=10)
        Resissue_total=Resissue.total

        Resissue_OT=jira.search_issues(jql_Resissue_OT,maxResults=10)
        Resissue_OT_total=Resissue_OT.total

        n=(unRes_issue_total,unRes_issue_OT_total,Resissue_total,Resissue_OT_total)

    elif jira==jira_jishu:
        if project_name=="财富端后台测试组":
            time = today - datetime.timedelta(days=14)

            jql_unResissue_jishu = "project=" + project_name + affectedVersion + str(
                version) + sign + ' and issuetype = 缺陷 AND status in(NEW,已确认) and createdDate >= '+str(time)+' ORDER BY created DESC'

            jql_unResissue_OT_jishu = "project=" + project_name + affectedVersion + str(
                version) + sign + ' and issuetype = 缺陷 and status in (NEW,Reopen,已确认' + ") AND created <= -24h and createdDate >= "+str(time)+" or (project=" + project_name + affectedVersion + str(
                version) + sign + ' and issuetype = 缺陷 and status = Reopened AND updated  <= 24h) and createdDate >= '+str(time)+' ORDER BY created DESC'

            jql_Resissue_jishu = "project=" + project_name + affectedVersion + str(
                version) + sign + ' and issuetype = 缺陷 AND status  in (无法复现,已修复) and createdDate >= '+str(time)+' ORDER BY created DESC'

            jql_Resissue_OT_jishu = "project=" + project_name + affectedVersion + str(
                version) + sign + ' and issuetype = 缺陷 and status  in (无法复现,已修复) AND updatedDate <= -24h and createdDate >= '+str(time)+' ORDER BY created DESC'

        unRes_issue = jira.search_issues(jql_unResissue_jishu, maxResults=10)
        unRes_issue_total = unRes_issue.total

        unRes_issue_OT = jira.search_issues(jql_unResissue_OT_jishu, maxResults=10)
        unRes_issue_OT_total = unRes_issue_OT.total

        Resissue = jira.search_issues(jql_Resissue_jishu, maxResults=10)
        Resissue_total = Resissue.total

        Resissue_OT = jira.search_issues(jql_Resissue_OT_jishu, maxResults=10)
        Resissue_OT_total = Resissue_OT.total

        n = (unRes_issue_total, unRes_issue_OT_total, Resissue_total, Resissue_OT_total)

    return n

def alter(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,str(new_str))
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)

def write_email(hot_project,issue_data,total,group_issue):

    path = os.getcwd() + "/Template/Email/"


    shutil.copy(path+"email.html", path+"em.html")
    
    m = []
    m1= []
    # 统计今日缺陷
    for i in range(len(hot_project)):
        project_name=hot_project[i][0]
        version=hot_project[i][1]
        create_time=hot_project[i][2]
        issue_count=hot_project[i][3]
        new_count=hot_project[i][4]
        resolved_count=hot_project[i][5]
        closed_count=hot_project[i][6]
        wontfix_count=hot_project[i][7]
        un_resolved_count=str(issue_data[i][3])
        unOt_resolved_count=str(issue_data[i][4])
        un_closed_count=str(issue_data[i][5])
        unOt_closed_count=str(issue_data[i][6])

        le = len(group_issue)



        data1 = group_issue[i]
        n = []
        for k, v in data1.items():
            group1 = k
            group1_data = v

            group = '<tbody><tr><td style="width:80%;">' + str(
                group1) + '</td><td style="width:20%;">' + str(group1_data) + "</td></tr></tbody>"
            n.append(group)

        n = ''.join(n)


        project = "<tr><td style='width:80'>"+project_name+"<br /></td><td style='width:17%'>"+version+"<br /></td><td style='width:8%'>"+create_time+"<br /></td><td style='width:8%'>"+\
                 str(issue_count)+ '</td><td>' + "<table" + ' style="width:130;" cellpadding="2" cellspacing="0" border="1" bordercolor="#000000">' + n+"</table>"+"<td style='width:8%'>"+str(wontfix_count)+"</td><td style='width:8%'>"+str(new_count)+"</td><td style='width:8%'>"+str(resolved_count)+"</td><td style='width:8%'>"\
                  +str(closed_count)+"</td><td style='color:red;width:7%'>"+un_resolved_count+"</td><td style='color:red;width:7%'>"+unOt_resolved_count+"</td><td style='color:red;width:7%'>"\
                  +un_closed_count+"</td><td style='color:red;width:7%'>"+unOt_closed_count+"</td></tr>"
        m.append(project)
    s1=''.join(m)

    # 统计未解决缺陷
    # for i in range(len(issue_data)):
    #     project_name=issue_data[i][0]
    #     version=issue_data[i][1]
    #     create_time = issue_data[i][2]
    #     un_resolved_count=str(issue_data[i][3])
    #     unOt_resolved_count=str(issue_data[i][4])
    #     un_closed_count=str(issue_data[i][5])
    #     unOt_closed_count=str(issue_data[i][6])
    #
    #     projet = "<td>"+un_resolved_count+"</td><td>"+unOt_resolved_count+"</td><td>"+un_closed_count+"</td><td>"+unOt_closed_count+"</td></tr>"
    #     m1.append(projet)
    # s2=''.join(m1)

    # 统计总和
    new_total=total[0]
    resloved_total=total[1]
    closed_total=total[2]
    unresolvde_total=total[3]
    unresolvde_ot_total=total[4]
    unclosed_total=total[5]
    unclosed_ot_total=total[6]
    wontfix_total=total[7]

    alter(path + "em.html", "${wontfix_total}", wontfix_total)
    alter(path+"em.html","${new_total}",new_total)
    alter(path + "em.html", "${resloved_total}", resloved_total)
    alter(path + "em.html", "${closed_total}", closed_total)

    alter(path + "em.html", "${unresolvde_total}", unresolvde_total)
    alter(path + "em.html", "${unresolvde_ot_total}", unresolvde_ot_total)
    alter(path + "em.html", "${unclosed_total}", unclosed_total)
    alter(path + "em.html", "${unclosed_ot_total}", unclosed_ot_total)


    alter(path+"em.html", "${project}",s1)
    # alter(path+"em.html", "${issue_data}",s2)

def takeSecond(elem):
    return elem[1]

def takeThree(elem):
    return elem[2]

def takeOne(elem):
    return elem[0]

def issue_group(group,project_name,version,jira):
    Simu=Yonghu=Qudao=Qianduan=YixinApp=YixinAppServer=CaifuBI=YrcaifuAPPServer=Dazhong=0

    Gpbx=YrzhiwangAPP=Zhifuzu=Ceshi=Gupiao=Chanpin=YirenH5=0


    affectedVersion = ' and affectedVersion = "'
    sign = '"'

    if version == "无":
        version = ''
        affectedVersion = ' and affectedVersion = EMPTY '

        sign = ''

    if project_name == "Capital Call":
        project_name = 'CC'

    if jira==jira_caifu:
        jql_allissue = "project=" + project_name + affectedVersion + str(version) + sign + ' And resolution in (Unresolved, Fixed, Incomplete, 重复提交) ORDER BY created DESC'

    elif jira==jira_jishu:

        if project_name=='财富端后台测试组':
            time = today - datetime.timedelta(days=14)

            jql_allissue = "project=" + project_name + affectedVersion + str(
                version) + sign + 'and issuetype = 缺陷 and createdDate >= '+str(time)+' ORDER BY created DESC'
        else:
            jql_allissue = "project=" + project_name + affectedVersion + str(version) + sign + ' and issuetype = 缺陷 ORDER BY created DESC'


    issues = jira.search_issues(jql_allissue, maxResults=500)

    for i in issues:
        try:
            assignee=jira.issue(i).fields.assignee.displayName
            assignee=assignee.replace(" ", "")
        except:
            assignee=" "
            logger.warning("缺陷"+str(i)+"经办人错误")


        if str(assignee) in group:

            if group[assignee] == "私募交易组":
                Simu += 1

            elif group[assignee] == "用户中心组":
                Yonghu += 1

            elif group[assignee] == "渠道服务组":
                Qudao +=1

            elif group[assignee] == "前端组":
                Qianduan += 1

            elif group[assignee] == "宜信财富APP组":
                YixinApp += 1

            elif group[assignee] == "宜信财富APP后端组":
                YixinAppServer += 1

            elif group[assignee] == "财富BI团队":
                CaifuBI += 1

            elif group[assignee] == "宜人指旺APP":
                YrzhiwangAPP += 1

            elif group[assignee] == "宜人财富APP后端":
                YrcaifuAPPServer += 1

            elif group[assignee] == "大众投资交易组":
                Dazhong += 1

            elif group[assignee] == "股票及保险团队":
                Gpbx +=1

            elif group[assignee] == "支付组":
                Zhifuzu +=1

            elif group[assignee] == "测试组":
                Ceshi += 1

            elif group[assignee] == "产品":
                Chanpin += 1

            elif group[assignee] == "股票业务组":
                Gupiao += 1
            elif group[assignee] == "宜人产品及H5":
                YirenH5 += 1
        else:
            logger.warning("缺陷"+str(i)+str(assignee))



    total=dict(zip(['私募交易组','用户中心组','渠道服务组','前端组','宜信财富APP组','宜信财富APP后端组','财富BI团队','宜人财富APP','宜人财富APP后端','大众投资交易组','股票及保险团队','支付组','测试组','产品组','股票业务组','宜人产品及H5'],
                   [Simu,Yonghu,Qudao,Qianduan,YixinApp,YixinAppServer,CaifuBI,YrzhiwangAPP,YrcaifuAPPServer,Dazhong,Gpbx,Zhifuzu,Ceshi,Chanpin,Gupiao,YirenH5]))
    return total

def data_clear(cleardata):
    # 去除字典中 value=0的数据
    for k in list(cleardata.keys()):
        if cleardata[k] == 0: del cleardata[k]
    return cleardata

def issue_count(project,jira):
    c=[]
    m=[]
    t=[]
    T_m=[]

    project_names=list(project.keys())
    logger.info(project_names)
    for i in range(len(project_names)):
        project_name=project_names[i]
        version=s[project_name]

        if len(version)==0:
            version=["无"]
        for j in range(len(version)):
            k=version[j][0]

            if k =="无":
                pass
            else:
                d=version_issue(project_name,k,jira)

            logger.info(project_name+str(k)+str(d))

            if str(d[1])>=str(expiryday) and d[1] !="该项目下无缺陷" and k !="无":
                hot_version=(project_name,version[j][0],d[1],d[0],d[2],d[3],d[4],d[5])
                logger.info(hot_version)

                x = issue_data(project_name, k,jira)
                logger.info(project_name + str(k) + str(x))

                issue_data1=(project_name,version[j][0],d[1],x[0],x[1],x[2],x[3])
                logger.info("issue_data1"+str(issue_data1))

                c.append(issue_data1)
                # c.sort(key=takeThree, reverse=True)

                m.append(hot_version)
                # m.sort(key=takeThree, reverse=True)

                b1=(issue_data1[3:7])
                t.append(b1)

                issue_g=issue_group(group,project_name,version[j][0],jira)
                cleat_group = data_clear(issue_g)
                pp=(d[1],cleat_group)


                T_m.append(pp)
                # T_m.sort(key=takeOne, reverse=True)
            else:

                logger.info(project_name+str(k)+"  "+d[1])

    return m,c,t,T_m

def today_total(today_issues,version_issues):
    new_total=0
    resloved_total=0
    closed_total=0
    wontfix_total=0

    unresolvde_total=0
    unresolvde_ot_total=0
    unclosed_total=0
    unclosed_ot_total=0



    for i in range(len(today_issues)):
        new_issue = today_issues[i][4]
        resloved_issue=today_issues[i][5]
        closed_issue=today_issues[i][6]
        wontfix_issue=today_issues[i][7]

        new_total += new_issue
        resloved_total += resloved_issue
        closed_total += closed_issue
        wontfix_total += wontfix_issue

    for j in range(len(version_issues)):
        unresolvde_issue = version_issues[j][3]
        unresolvde_ot_issue = version_issues[j][4]
        unclosed_issue = version_issues[j][5]
        unclosed_ot_issue = version_issues[j][6]

        unresolvde_total += unresolvde_issue
        unresolvde_ot_total += unresolvde_ot_issue
        unclosed_total += unclosed_issue
        unclosed_ot_total += unclosed_ot_issue

    return new_total,resloved_total,closed_total,unresolvde_total,unresolvde_ot_total,unclosed_total,unclosed_ot_total,wontfix_total

def trust(file_name):
    # 声明一个空字典，来保存文本文件数据
    dict_temp = {}
    os_path=os.getcwd()+"/Template/"
    file=os_path+file_name
    # 打开文本文件
    file = open(file, 'r',encoding = 'UTF-8')

    # 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    for line in file.readlines():
        line = line.strip()
        k = line.split(' ')[0]
        v = line.split(' ')[1]

        dict_temp[k] = v

    # 依旧是关闭文件
    file.close()
    return dict_temp


if __name__ == '__main__':

    logging.config.fileConfig('logging.conf')
    logger=logging.getLogger('simpleFormatter')

    today = datetime.date.today()
    expiryday= today - datetime.timedelta(days=30)

    logging.info("有效时间"+str(expiryday))

    jira_caifu = JIRA()

    jira_jishu = JIRA(basic_auth=(''),options = {'server':''})



    today_issues_title = [('项目名称', '最新迭代版本', '最近问题创建时间', '问题总数',"won't fix问题", '今日新建问题', '今日解决问题', '今日关闭问题')]
    version_issues_title = [('迭代版本未解决BUG数', '迭代版本超时（24小时）未解决BUG数', '迭代版本未关闭BUG数', '迭代版本超时（24小时）未关闭BUG数')]

    all_today_issues=[]
    all_version_issues=[]
    total=()
    all_group_issue1=[]
    all_excel_data =[]

    for i in [jira_jishu,jira_caifu]:
        s = project(i)

        logger.info(s)
        group = trust('user.txt')
        detail=issue_count(s,i)

        today_issues=detail[0]
        version_issues=detail[1]
        group_issue=detail[3]
        excel_data=[]

        group_issue1=[]
        for i in range(len(group_issue)):
            group_issue1.append(group_issue[i][1])

        for i in range(len(version_issues)):
            excel_data1=version_issues[i][3:7]
            excel_data.append(excel_data1)

        for m in range(len(today_issues)):

            all_today_issues.append(today_issues[m])
            all_version_issues.append(version_issues[m])
            all_group_issue1.append(group_issue1[m])

            all_excel_data.append(excel_data[m])

    logging.info("今日缺陷"+str(all_today_issues))
    logging.info("版本缺陷汇总"+str(all_version_issues))
    logging.info("分组情况"+str(all_group_issue1))


    total = today_total(all_today_issues,all_version_issues)


    write_email(all_today_issues,all_version_issues,total,all_group_issue1)
    excel_name=str(datetime.date.today())+"BUG统计"

    a=today_issues_title+all_today_issues
    b=version_issues_title+all_excel_data

    # excel.write(excel_name,a,b,group_issue1)

    all_group_issue1 = ["缺陷分组"] + all_group_issue1

    excel.write(excel_name,a,b,all_group_issue1)

    with open(os.getcwd()+'/Template/'+'recevers.txt','r') as f:
        recevers = f.read().splitlines()

    sendEmail.send_email(excel_name,recevers,"em.html")
