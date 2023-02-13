from collections import defaultdict
from atlassian import Jira


class JiraBoard:
    def __init__(self, jira_url, jira_user_name, jira_api_token):
        self.jira = Jira(
            url=jira_url,
            username=jira_user_name,
            password=jira_api_token,
            cloud=True
        )

    def get_issues(self, board: str, status: str):
        jql = f"project = '{board}' AND status in {status} order by fixVersion ASC"

        issues = self.jira.jql(jql)["issues"]

        issue_infos = defaultdict(list)
        for issue in issues:
            version = self._get_issue_fix_version(issue)
            issue_infos[version].append({
                "epic": self._get_issue_epic(issue),
                "key": self._get_issue_key(issue),
                "title": self._get_issue_title(issue),
                "assignee": self._get_issue_assignee(issue),
                "link": self._get_issue_link(issue),
                "status": self._get_issue_status(issue),
            })

        return issue_infos

    def _get_issue_fix_version(self, issue):
        versions = issue['fields']['fixVersions']
        if versions:
            return versions[0]['name']
        return '버전이 할당되지 않은 티켓'

    def _get_issue_epic(self, issue):
        if issue['fields'].get('parent'):
            return issue['fields']['parent']['fields']['summary']
        return 'No Epic'

    def _get_issue_key(self, issue):
        return issue['key']

    def _get_issue_status(self, issue):
        return issue['fields']['status']['name']

    def _get_issue_title(self, issue):
        title = issue['fields']['summary']
        return title[:25] + '...' if len(title) > 25 else title

    def _get_issue_assignee(self, issue):
        if issue['fields']['assignee']:
            return issue['fields']['assignee']['displayName']
        return 'No Assignee'

    def _get_issue_link(self, issue):
        return f"https://greppcorp.atlassian.net/browse/{issue['key']}"
