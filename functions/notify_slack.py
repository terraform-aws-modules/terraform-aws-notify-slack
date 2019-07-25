from __future__ import print_function
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
                    "value": "https://console.aws.amazon.com/cloudwatch/home?region=" + region + "#alarm:alarmFilter=ANY;name=" + urllib.parse.quote_plus(message['AlarmName']),
                    "short": False
                }
            ]
        }
    
def ecs_notification(message, region):
    states = {'RUNNING': 'good', 'PENDING': 'warning', 'PROVISIONING': 'warning', 'DEPROVISIONING': 'warning', 'ACTIVATING': 'warning', 'DEACTIVATING': 'warning', 'STOPPING': 'danger', 'STOPPED': 'danger'}

    return {
            "color": states[message['detail']['lastStatus']],
            "fallback": "ECS {} triggered".format(message['detail']),
            "fields": [
                { "title": "lastStatus", "value": message['detail']['lastStatus'], "short": True },
                { "title": "desiredStatus", "value": message['detail']['desiredStatus'], "short": True },
                { "title": "taskDefinitionArn", "value": message['detail']['taskDefinitionArn'], "short": False },
                { "title": "group", "value": message['detail']['group'], "short": True },
                { "title": "time", "value": message['time'], "short": True}
            ]
        }
        
def ectwo_notification(message, region):
    return {
            "color": 'good',
            "fallback": "EC2 {} event".format(message['detail']),
            "fields": [
                { "title": "account", "value": message['account'], "short": True },
                { "title": "region", "value": message['region'], "short": True },
                { "title": "user", "value": message['detail']['userIdentity']['principalId'], "short": True },
                { "title": "event", "value": message['detail']['eventName'], "short": True },
                { "title": "ip", "value": message['detail']['sourceIPAddress'], "short": True },
                { "title": "time", "value": message['time'], "short": True}
            ]
        }

def rds_notification(message, region):
    return {
            "color": 'good',
            "fallback": "RDS {} event".format(message['detail']),
            "fields": [
                { "title": "account", "value": message['account'], "short": True },
                { "title": "region", "value": message['region'], "short": True },
                { "title": "resources", "value": message['resources'][0], "short": False },
                { "title": "message", "value": message['detail']['Message'], "short": True },
                { "title": "time", "value": message['time'], "short": True}
            ]
        }
        
def iam_notification(message, region):
    return {
            "color": 'good',
            "fallback": "IAM {} event".format(message['detail']),
            "fields": [
                { "title": "account", "value": message['account'], "short": True },
                { "title": "region", "value": message['region'], "short": True },
                { "title": "user", "value": message['detail']['userIdentity']['principalId'], "short": False },
                { "title": "message", "value": message['detail']['eventName'], "short": True },
                { "title": "ip", "value": message['detail']['sourceIPAddress'], "short": True },
                { "title": "time", "value": message['time'], "short": True}
            ]
        }

def default_notification(subject, message):
    return {
            "fallback": "A new message",
            "fields": [{"title": subject if subject else "Message", "value": json.dumps(message), "short": False}]
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
        payload['text'] = "AWS CloudWatch notification - " + message['AlarmName']
        payload['attachments'].append(notification)
    elif ("source" in message and message['source'] == "aws.ecs"):
        notification = ecs_notification(message, region)
        payload['text'] = "AWS ECS notification - " + message["detail-type"]
        payload['attachments'].append(notification)
    elif ("source" in message and message['source'] == "aws.ec2"):
        notification = ectwo_notification(message, region)
        payload['text'] = "AWS EC2 notification - " + message["detail-type"]
        payload['attachments'].append(notification)
    elif ("source" in message and message['source'] == "aws.rds"):
        notification = rds_notification(message, region)
        payload['text'] = "AWS RDS notification - " + message["detail-type"]
        payload['attachments'].append(notification)
    elif ("source" in message and message['source'] == "aws.iam"):
        notification = iam_notification(message, region)
        payload['text'] = "AWS IAM notification - " + message["detail-type"]
        payload['attachments'].append(notification)
    else:
        payload['text'] = "AWS notification"
        payload['attachments'].append(default_notification(subject, message))

    data = urllib.parse.urlencode({"payload": json.dumps(payload)}).encode("utf-8")
    req = urllib.request.Request(slack_url)
    urllib.request.urlopen(req, data)


def lambda_handler(event, context):
    subject = event['Records'][0]['Sns']['Subject']
    message = event['Records'][0]['Sns']['Message']
    region = event['Records'][0]['Sns']['TopicArn'].split(":")[3]
    notify_slack(subject, message, region)

    return message

#notify_slack({"AlarmName":"Example","AlarmDescription":"Example alarm description.","AWSAccountId":"000000000000","NewStateValue":"ALARM","NewStateReason":"Threshold Crossed","StateChangeTime":"2017-01-12T16:30:42.236+0000","Region":"EU - Ireland","OldStateValue":"OK"}, "eu-west-1")
