from __future__ import print_function
import os, boto3, json, base64, datetime
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
        logging.exception("Error: failed to decrypt URL with KMS")

def format_log_url(region, logGroupName, Period, EvaluationPeriods):
    end = datetime.datetime.utcnow().replace(microsecond=0)
    start = end - datetime.timedelta(seconds=Period*EvaluationPeriods)
    return f"https://console.aws.amazon.com/cloudwatch/home?region={region}#logEventViewer:group={urllib.parse.quote_plus(logGroupName)};start={start.isoformat()}Z;end={end.isoformat()}Z"

def try_get_log_url(region, AlarmName):
    try:
        cloudwatch = boto3.client("cloudwatch")
        logs = boto3.client("logs")
        
        alarm = cloudwatch.describe_alarms(AlarmNames=[AlarmName])
        MetricName = alarm["MetricAlarms"][0]["MetricName"]
        Namespace = alarm["MetricAlarms"][0]["Namespace"]
        Period = alarm["MetricAlarms"][0]["Period"]
        EvaluationPeriods = alarm["MetricAlarms"][0]["EvaluationPeriods"]
        
        metric_filter = logs.describe_metric_filters(metricName=MetricName, metricNamespace=Namespace)
        try:
            logGroupName = metric_filter["metricFilters"][0]["logGroupName"]
        except KeyError, IndexError:
            return None
        if len(logGroupName) == 0:
            return None
        return format_log_url(region, logGroupName, Period, EvaluationPeriods)
    except Exception:
        logging.exception("Error: try_get_log_url failed")
        return None

def cloudwatch_notification(message, region):
    states = {'OK': 'good', 'INSUFFICIENT_DATA': 'warning', 'ALARM': 'danger'}

    result = {
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
    log_url = try_get_log_url(region, message['AlarmName'])
    # Attach log url for convenient log look up if log exists for the alarm
    if log_url:
        result["fields"].append({
            "title": "Link to Log",
            "value": log_url,
            "short": False
        })
    return result


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
        payload['text'] = "AWS CloudWatch notification - " + message["AlarmName"]
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
