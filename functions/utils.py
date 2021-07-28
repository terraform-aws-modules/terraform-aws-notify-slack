import json
import os
import logging
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


LOG = logging.getLogger(__name__)


class LocalSlack:
  @staticmethod
  def send_message(channel, subject, message):
    if slack_api_token := os.environ.get('SLACK_API_TOKEN'):
      LOG.info(f"Found SLACK_API_TOKEN, posting slack message: {message}")
      slack_api_token = os.environ.get('SLACK_API_TOKEN') or get_secrets()
      client = Slack(slack_api_token, os.environ['ENV'])
      return client.send_message(channel, subject, message)
    else:
      LOG.info("SLACK_API_TOKEN is not set - logging message")
      LOG.info(f"{channel}: {message}")
      return {"ok": True} 

class Slack:
  def __init__(self, slack_api_token, env):
    self.client = WebClient(token=slack_api_token)
    self.env = env

  def send_message(self, channel, subject, message):
    return self.client.chat_postMessage(
      channel=channel,
      blocks=[
          {
            "type": "header",
            "text": {
              "type": "plain_text",
              "text": subject,
              "emoji": True
            }
          },
          {
              "type": "section",
              "text": {
                  "type": "mrkdwn",
                  "text": message
              }
          },
          {
              "type": "context",
              "elements": [
                  {
                      "type": "plain_text",
                      "text": f"ENV: {self.env}"
                  }
              ]
          }
      ])


@lru_cache(maxsize=1)
def get_slack():
  """
  :return: SlackObject
  """
  env = os.getenv('ENV', 'local')
  if env not in ['testing', 'local']:
    slack_api_token = os.environ.get('SLACK_API_TOKEN') or get_secrets()
    slack = Slack(slack_api_token, env)
    if not slack.auth_test().get('ok', False):
      raise SlackApiError("Could not authenticate Slack WebClient using env api_token")
  else:
    return LocalSlack()

