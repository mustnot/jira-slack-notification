import os
import requests
from atlassian import Jira


SLACK_HOOK_URL = os.environ.get('SLACK_HOOK_URL')
JIRA_URL = os.environ.get('JIRA_URL')
JIRA_USER_NAME = os.environ.get('JIRA_USER_NAME')
JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')


class PEDUSlackNotification:
    
    def __init__(self, jira_url, jira_user_name, jira_api_token, slack_hook_url):
        self.jira = Jira(
            url=jira_url,
            username=jira_user_name,
            password=jira_api_token,
            cloud=True
        )
        self.slack_hook_url = slack_hook_url

    def get_issues(self, jql):
        return self.jira.jql(jql)["issues"]

    def send_slack_notification(self, issues):
        blocks = []

        header_block = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Alpha Tested Issues"
            }
        }

        section_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "제목"
            }
        }

        divider_block = {
            "type": "divider"
        }

        blocks.append(header_block)
        blocks.append(divider_block)

        issues_blocks = []
        for issue in issues:
            title = issue['fields']['summary']
            assignee = issue['fields']['assignee']['displayName']
            link = f"https://greppcorp.atlassian.net/browse/{issue['key']}"

            versions = issue['fields']['fixVersions']

            version = '지정된 버전이 없음'
            if versions:
                version = versions[0]['name']

            section_block['text']['text'] = f"<{link}|{version} - {title} - {assignee}>"

            issues_blocks.append(section_block)

        issues_blocks.sort(key=lambda x: x['text']['text'])

        requests.post(self.slack_hook_url, json={"blocks": blocks + issues_blocks})


if __name__ == '__main__':
    jql = '''project = PEDU AND status="Alpha Tested" order by fixVersion ASC'''
    pedu_slack_notification = PEDUSlackNotification(JIRA_URL, JIRA_USER_NAME, JIRA_API_TOKEN, SLACK_HOOK_URL)
    issues = pedu_slack_notification.get_issues(jql)
    pedu_slack_notification.send_slack_notification(issues)