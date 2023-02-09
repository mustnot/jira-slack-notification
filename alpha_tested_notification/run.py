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
    blocks.append(slack.header_block('오늘 배포할 티켓을 확인해 주세요.'))
    blocks.append(slack.divider_block())

    for issue in jira.get_issues('PEDU', 'Alpha Tested'):
        messages = []
        messages.append(f"[<{issue['link']}|{issue['key']}>]")
        messages.append(f"{issue['title']}")
        messages.append(f"({issue['assignee']})")
        messages.append(f"- {issue['version']}")


        blocks.append(slack.section_block(" ".join(messages)))

    slack.send_message(blocks)