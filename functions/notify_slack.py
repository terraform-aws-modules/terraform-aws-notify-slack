from __future__ import print_function
from urllib.error import HTTPError
import os, boto3, json, base64
import urllib.request, urllib.parse
import logging

from slack_sdk.errors import SlackApiError
from utils import get_slack

# Decrypt encrypted URL with KMS
def decrypt(encrypted_url):
  region = os.environ['AWS_REGION']
  try:
    kms = boto3.client('kms', region_name=region)
    plaintext = kms.decrypt(CiphertextBlob=base64.b64decode(encrypted_url))['Plaintext']
    return plaintext.decode()
  except Exception:
    logging.exception("Failed to decrypt URL with KMS")


def cloudwatch_notification(message, region):
  states = {'OK': 'good', 'INSUFFICIENT_DATA': 'warning', 'ALARM': 'danger'}
  if region.startswith("us-gov-"):
    cloudwatch_url = "https://console.amazonaws-us-gov.com/cloudwatch/home?region="
  else:
    cloudwatch_url = "https://console.aws.amazon.com/cloudwatch/home?region="

  return {
    "color": states[message['NewStateValue']],
    "fallback": "Alarm {} triggered".format(message['AlarmName']),
    "fields": [
      { "title": "Alarm Name", "value": message['AlarmName'], "short": True },
      { "title": "Alarm Description", "value": message['AlarmDescription'], "short": False},
      { "title": "Alarm reason", "value": message['NewStateReason'], "short": False},
      { "title": "Old State", "value": message['OldStateValue'], "short": True },
      { "title": "Current State", "value": message['NewStateValue'], "short": True },
      {
        "title": "Link to Alarm",
        "value": cloudwatch_url + region + "#alarm:alarmFilter=ANY;name=" + urllib.parse.quote(message['AlarmName']),
        "short": False
      }
    ]
  }


def default_notification(subject, message):
  attachments = {
    "fallback": "A new message",
    "title": subject if subject else "Message",
    "mrkdwn_in": ["value"],
    "fields": []
  }
  if type(message) is dict:
    for k, v in message.items():
      value = f"`{json.dumps(v)}`" if isinstance(v, (dict, list)) else str(v)
      attachments['fields'].append(
        {
          "title": k,
          "value": value,
          "short": len(value) < 25
        }
      )
  else:
    attachments['fields'].append({"value": message, "short": False})

  return attachments


# Send a message to a slack channel
def notify_slack(subject, message, region):
  if not (slack_channels := os.environ.get('SLACK_CHANNELS')):
    raise ValueError("Env var SLACK_CHANNELS is not set! Check the configuration")

  slack_channels = slack_channels.split(',')
  slack_users = os.environ.get('SLACK_USERS', '').split(',')
  slack_groups = os.environ.get('SLACK_GROUPS', '').split(',')
  slack_emoji = os.environ.get('SLACK_EMOJI', ':aws:')

  payload = {
    "region": region,
    "channels": slack_channels,
    "users": slack_users,
    "groups": slack_groups,
    "icon_emoji": slack_emoji,
    "attachments": [],
    "msgs_sent": 0,
  }

  # Convert the message from a json string to a dict
  if isinstance(message, str):
    try:
      message = json.loads(message)
    except json.JSONDecodeError as err:
      logging.info(f'No JSON in SNS message, using the SNS message as the slack msg - err: {err}')
      message = {'text': message}

  text = ""
  # Don't add extra lines unless there are values to iterate on
  if len(slack_users) > 0 and slack_users[0] :
    text += '\n' + ", ".join('<@' + whom + '>' for whom in slack_users if whom != '')
  if len(slack_groups) > 0:
    text += '\n' + ", ".join('<!subteam^' + group + '>' for group in slack_groups if group != '')
  text += '\n'

  # Based on the notification type, format text
  if alarm_name := message.get("AlarmName") in message:
    notification = cloudwatch_notification(message, region)
    payload['text'] = text + "AWS CloudWatch notification - " + alarm_name
  elif "text" in message:
    payload['text'] = text + message['text']
  else:
    payload['text'] = text + "AWS notification"

  slack = get_slack()
  for channel in slack_channels:
    response = slack.send_message(channel, subject, payload['text'])
    payload['msgs_sent'] += 1
    logging.debug(f"Sent slack message to {channel} - success={response.get('ok', False)}")

  return payload

def lambda_handler(event, context):
  if os.environ.get('LOG_EVENTS', 'False').title() == 'True':
    logging.warning('Event logging enabled: `{}`'.format(json.dumps(event)))

  subject = event['Records'][0]['Sns']['Subject']
  message = event['Records'][0]['Sns']['Message']
  region = event['Records'][0]['Sns']['TopicArn'].split(":")[3]

  response = notify_slack(subject, message, region)
  return {
      'statusCode': 200,
      'headers': {
        'Content-Type': 'application/json'
      },
      'body': json.dumps(response)
  }


if __name__ == "__main__":
  from notify_slack_test import events
  logging.getLogger().setLevel(logging.DEBUG)
  for event in events:
    response = notify_slack('subject', event, 'eu-west-1')
