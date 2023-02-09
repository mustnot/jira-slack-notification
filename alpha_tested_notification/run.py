import os

from jira import JiraBoard
from slack import Slack


SLACK_HOOK_URL = os.environ.get('SLACK_HOOK_URL')
JIRA_URL = os.environ.get('JIRA_URL')
JIRA_USER_NAME = os.environ.get('JIRA_USER_NAME')
JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')


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