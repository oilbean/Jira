from jira import JIRA
import Excel
import logging
import logging.config


def project():
    p_name=[]
    projects=jira.projects()
    for i in range(len(projects)):
        p_name.append(projects[i].name)

    return p_name

#统计每个项目问题总数、未解决问题数、最新问题创建时间
def issue_count(p_name):

    jql="project='"+ p_name + "'ORDER BY created DESC"

    project_issue=jira.search_issues(jql,maxResults=10)
    logger.info("查询项目：" + p_name +"   查询语句"+jql)
    issue_total = project_issue.total
    logger.info("获取"+p_name+"缺陷数量:"+str(issue_total))

    if issue_total !=0:
        new_credit=project_issue[0]
        new_credit_time=jira.issue(new_credit,fields='created').fields.created
        new_credit_time=new_credit_time[0:10]
        logger.info("获取" + p_name + "最新问题创建时间:" + new_credit_time)
    else:
        new_credit_time="该项目下无缺陷"
        logger.info("获取" + p_name + "最新问题创建时间:" + new_credit_time)

    Opissue = jira.search_issues("project = '" + p_name + "' AND status in (Open, 'In Progress', Reopened)")
    Opissue_total = Opissue.total
    logger.info("获取" + p_name + "未解决缺陷数量:" +str(Opissue_total))


    return p_name,issue_total,Opissue_total,new_credit_time

def find_issue(jql,maxR=500):

    issues=jira.search_issues(jql,maxResults=maxR)
    logger.info("缺陷查询：查询语句" + jql)

    issues_total=issues.total
    logger.info("获取缺陷数量:" + str(issues_total))
    t=maxR
    while t<issues_total:
        logger.info("缺陷查询：查询下一页")
        issue_other=jira.search_issues(jql,startAt=t,maxResults=maxR)

        issues=issues+issue_other
        t+=maxR

    issue_result={}
    issue_result['问题总数']=issues_total

    a=[]
    if issues_total !=0:
        for issue in issues:
            key=issue.fields.project.name

            a.append(key)

        for key in set(a):
            issue_result[key] = a.count(key)
            logger.info("获取项目" + key+"缺陷数量"+str(issue_result[key]))
    return issue_result


if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')
    logger=logging.getLogger('simpleFormatter')

    # 统计24小时内未解决问题
    jql="status in (Open, 'In Progress') AND created <= -24h or (status = Reopened AND updated  <= 24h) ORDER BY created DESC"
    # 统计24小时内未关闭问题
    jql_1="status = Resolved AND resolved <= -24h ORDER BY created DESC"

    jira = JIRA('url', basic_auth=('name', 'password'))

    a=[]
    s=project()
    for i in range(len(s)):
        p=issue_count(s[i])
        a.append(p)

    b=find_issue(jql)
    c=find_issue(jql_1)
    Excel.write(a,"项目汇总")
    Excel.write(b,"24小时内未解决问题")
    Excel.write(c,"24小时内未关闭问题")

