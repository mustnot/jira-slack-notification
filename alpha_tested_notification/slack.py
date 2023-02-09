import requests


class Slack:
    def __init__(self, slack_hook_url:str):
        self.slack_hook_url = slack_hook_url

    def header_block(self, text:str):
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": text
            }
        }

    def title_block(self, text:str):
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{text}*"
            }
        }

    def text_block(self, text:str):
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }

    def quote_block(self, text:str):
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"> {text}"
            }
        }

    def divider_block(self):
        return {
            "type": "divider"
        }

    def send_message(self, blocks:list):
        requests.post(self.slack_hook_url, json={"blocks": blocks})