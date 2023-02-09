import os

from jira import JiraBoard
from slack import Slack


# SLACK_HOOK_URL = os.environ.get('SLACK_HOOK_URL')
# JIRA_URL = os.environ.get('JIRA_URL')
# JIRA_USER_NAME = os.environ.get('JIRA_USER_NAME')
# JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')

SLACK_HOOK_URL = 'https://hooks.slack.com/services/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'
JIRA_URL = 'https://greppcorp.atlassian.net'
JIRA_USER_NAME = 'jade@grepp.co'
JIRA_API_TOKEN = 'ATATT3xFfGF0tMP_r2shWAlGqbI4q1o1RGCopG25yfQsd9w2_Yt_XLQKBrjQMQ0Kvg8W0sUmwj8dEk8iYPiV9_ZdbQH15vdIX9EDQEdtJvPX_NlUmpbZFcxFFW7iRdhzgG6yWXj80wLmYD4iUOnhQfFdGY6-Pd_86-4SW1WfByL4gQGzH1z4lf4=7EA9A5B7'



if __name__ == '__main__':
    jira = JiraBoard(JIRA_URL, JIRA_USER_NAME, JIRA_API_TOKEN)
    slack = Slack(SLACK_HOOK_URL)
    
    blocks = []
    blocks.append(slack.header_block('오늘 배포할 티켓을 확인해주세요.'))
    blocks.append(slack.divider_block())

    alpha_tested_issue_infos = jira.get_issues('PEDU', ('Alpha Tested', 'In Alpha'))
    for key, issues in sorted(alpha_tested_issue_infos.items(), key=lambda x: x[0]):
        blocks.append(slack.title_block(key))

        messages = []
        for index, issue in enumerate(sorted(issues, key=lambda x: x['status'])):
            message = []
            message.append(f"{index+1}.")
            message.append(f"[<{issue['link']}|{issue['key']}>]")
            message.append(f"{issue['title']}")
            message.append(f"({issue['assignee']})")
            message.append(f"`{issue['status']}`")

            messages.append(" ".join(message))
        
        blocks.append(slack.quote_block("\n>".join(messages)))

    slack.send_message(blocks)