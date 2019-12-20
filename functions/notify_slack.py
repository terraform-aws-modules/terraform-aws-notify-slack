from __future__ import print_function
from urllib.error import HTTPError
import os, boto3, json, base64
import urllib.request, urllib.parse
import logging


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
        "value": "https://console.aws.amazon.com/cloudwatch/home?region=" + region + "#alarm:alarmFilter=ANY;name=" + urllib.parse.quote(message['AlarmName']),
        "short": False
      }
    ]
  }


def default_notification(subject, message):
  return {
    "fallback": "A new message",
    "fields": [{"title": subject if subject else "Message", "value": json.dumps(message) if type(message) is dict else message, "short": False}]
  }


# Send a message to a slack channel
def notify_slack(subject, message, region):
  slack_url = os.environ['SLACK_WEBHOOK_URL']
  if not slack_url.startswith("http"):
    slack_url = decrypt(slack_url)

  slack_channel = os.environ['SLACK_CHANNEL']
  slack_username = os.environ['SLACK_USERNAME']
  slack_emoji = os.environ['SLACK_EMOJI']

  payload = {
    "channel": slack_channel,
    "username": slack_username,
    "icon_emoji": slack_emoji,
    "attachments": []
  }

  if type(message) is str:
    try:
      message = json.loads(message)
    except json.JSONDecodeError as err:
      logging.exception(f'JSON decode error: {err}')

  if "AlarmName" in message:
    notification = cloudwatch_notification(message, region)
    payload['text'] = "AWS CloudWatch notification - " + message["AlarmName"]
    payload['attachments'].append(notification)
  else:
    payload['text'] = "AWS notification"
    payload['attachments'].append(default_notification(subject, message))

  data = urllib.parse.urlencode({"payload": json.dumps(payload)}).encode("utf-8")
  req = urllib.request.Request(slack_url)

  try:
    result = urllib.request.urlopen(req, data)
    return json.dumps({"code": result.getcode(), "info": result.info().as_string()})

  except HTTPError as e:
    logging.error("{}: result".format(e))
    return json.dumps({"code": e.getcode(), "info": e.info().as_string()})


def lambda_handler(event, context):
  if 'LOG_EVENTS' in os.environ and os.environ['LOG_EVENTS'] == 'True':
    logging.warning('Event logging enabled: `{}`'.format(json.dumps(event)))

  subject = event['Records'][0]['Sns']['Subject']
  message = event['Records'][0]['Sns']['Message']
  region = event['Records'][0]['Sns']['TopicArn'].split(":")[3]
  response = notify_slack(subject, message, region)

  if json.loads(response)["code"] != 200:
    logging.error("Error: received status `{}` using event `{}` and context `{}`".format(json.loads(response)["info"], event, context))

  return response
