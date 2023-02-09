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
        jql = f"project = '{board}' AND status='{status}' order by fixVersion ASC"

        issues = self.jira.jql(jql)["issues"]

        issue_infos = []
        for issue in issues:
            issue_infos.append({
                "title": self._get_issue_title(issue),
                "assignee": self_._get_issue_assignee(issue),
                "link": self._get_issue_link(issue),
                "version": self._get_issue_fix_version(issue)
            })

        return issue_infos

    def _get_issue_fix_version(self, issue):
        versions = issue['fields']['fixVersions']
        if versions:
            return versions[0]['name']
        return '지정된 버전이 없음'

    def _get_issue_key(self, issue):
        return issue['key']

    def _get_issue_title(self, issue):
        return issue['fields']['summary']

    def _get_issue_assignee(self, issue):
        return issue['fields']['assignee']['displayName']

    def _get_issue_link(self, issue):
        return f"https://greppcorp.atlassian.net/browse/{issue['key']}"
