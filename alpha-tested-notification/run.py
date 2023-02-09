import os

from .jira import JiraBoard
from .slack import Slack


SLACK_HOOK_URL = os.environ.get('SLACK_HOOK_URL')
JIRA_URL = os.environ.get('JIRA_URL')
JIRA_USER_NAME = os.environ.get('JIRA_USER_NAME')
JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')


if __name__ == '__main__':
    jira = JiraBoard(JIRA_URL, JIRA_USER_NAME, JIRA_API_TOKEN)
    slack = Slack(SLACK_HOOK_URL)
    
    issues = jira.get_issues(jql)

    blocks = []
    blocks.append(slack.header_block('Alpha Tested Issues'))
    blocks.append(slack.divider_block())

    for issue in jira.get_issues('PEDU', 'Alpha Tested'):
        texts = []
        texts.append(f"[<{issue['link']}|{issue['key']}>]")
        texts.append(f"{issue['title']}")
        texts.append(f"({issue['assignee']})")
        texts.append(f"-{issue['version']}")


        blocks.append(slack.section_block(''.join(texts))))

    slack.send_message(blocks)