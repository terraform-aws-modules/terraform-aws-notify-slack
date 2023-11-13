from __future__ import print_function
import os, boto3, json, base64
import urllib.request, urllib.parse
import logging
import pprint
import re


# Decrypt encrypted URL with KMS
def decrypt(encrypted_url):
    region = os.environ['AWS_REGION']
    try:
        kms = boto3.client('kms', region_name=region)
        plaintext = kms.decrypt(CiphertextBlob=base64.b64decode(encrypted_url))['Plaintext']
        return plaintext.decode()
    except Exception:
        logging.exception("Failed to decrypt URL with KMS")

def ecr_notification(message, region):
    state = 'danger' if message.get('detail', {}).get('scan-status', "") == 'FAILED' else 'warning'
    return {
        "color": state,
        "fallback": "ECR {} event".format(message['detail']),
        "fields": [
            { "title": "Status", "value": message.get('detail', {}).get('scan-status', ""), "short": True },
            { "title": "Repo", "value": message.get('detail', {}).get('repository-name', ""), "short": True },
            { "title": "Tags", "value": ",".join(message.get('detail', {}).get('image-tags', [])), "short": True },
            { "title": "SHA", "value": message.get('detail', {}).get('image-digest', ""), "short": True },
            { "title": "CRITICAL", "value": message.get('detail', {}).get('finding-severity-counts', {}).get('CRITICAL', ""), "short": True },
            { "title": "HIGH", "value": message.get('detail', {}).get('finding-severity-counts', {}).get('HIGH', "0"), "short": True },
            {
                "title": "Link to Scan Results",
                "value": "https://console.aws.amazon.com/ecr/repositories/private/" + message['account'] + "/" + message.get('detail', {}).get('repository-name', "") + "/_/image/" + message.get('detail', {}).get('image-digest', "") + "/scan-results/?region=" + region,
                "short": False
            }
        ]
    }

def inspector_notification(message, region):
  state = 'good' if message.get('detail', {}).get('status', "") == 'CLOSED' else 'danger'
  return {
    "color": state,
    "fallback": "Inspector {} event".format(message['detail']),
    "fields": [
      { "title": "Title", "value": message.get('detail', {}).get('title', ""), "short": True },
      { "title": "Resource", "value": message['resources'][0], "short": True },
      { "title": "Severity", "value": message.get('detail', {}).get('severity', ""), "short": True },
      { "title": "Region", "value": message['region'], "short": True },
      { "title": "Account", "value": message.get('detail', {}).get('awsAccountId', ""), "short": True },
      { "title": "Status", "value": message.get('detail', {}).get('status', ""), "short": True },
      {
        "title": "Link to Scan Results",
        "value": "https://console.aws.amazon.com/inspector/v2/home?region=" + message['region'] + "#/findings/instances/" + message['resources'][0],
        "short": False
      }
    ]
  }

def asg_notification(message, regions):
    state = 'danger' if message.get("StatusCode", "") == 'Failed' else 'good'
    return {
        "color": state,
        "fallback": "ASG {} event".format(message['Description']),
        "fields": [
            { "title": "account", "value": message.get('AccountId', ""), "short": True },
            { "title": "progress", "value": message.get('Progress', ""), "short": True },
            { "title": "description", "value": message.get('Description', ""), "short": True },
            { "title": "asg name", "value": message.get('AutoScalingGroupName', ""), "short": True },
            { "title": "status code", "value": message.get('StatusCode', ""), "short": True }
        ]
    }

def cloudwatch_notification(message, region):
    states = {'OK': 'good', 'INSUFFICIENT_DATA': 'warning', 'ALARM': 'danger'}

    return {
            "color": states.get(message['NewStateValue'], "danger"),
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

    fields = []

    if message.get("detail", {}).get('stoppedReason', 'NOTFOUND') != 'NOTFOUND':
      fields.append( { "title": "stoppedReason", "value": message.get('detail', {}).get('stoppedReason', ""), "short": True })

    if message.get("detail", {}).get('stopCode', 'NOTFOUND') != 'NOTFOUND':
      fields.append( { "title": "stopCode", "value": message.get('detail', {}).get('stopCode', ""), "short": True })

    for key in message['detail']['containers']:
      if 'reason' in key:
        fields.append( { "title": "reason", "value": key['reason'], "short": True } )
        fields.append( { "title": "containerName", "value": key['name'], "short": True } )

    if message.get("detail", {}).get('eventName', 'NOTFOUND') == 'UpdateService':
      fields.append( { "title": "eventName", "value": "UpdateService", "short": True })
      fields.append( { "title": "principalId", "value":  message.get("detail", {}).get('userIdentity', {}).get('principalId', "???"), "short": True })
    else:
      fields.append({ "title": "lastStatus", "value": message.get('detail', {}).get('lastStatus', ""), "short": True })
      fields.append({ "title": "desiredStatus", "value": message.get('detail', {}).get('desiredStatus', ""), "short": True })

    if message.get("detail", {}).get('taskArn', 'NOTFOUND') != 'NOTFOUND':
      fields.append({ "title": "taskArn", "value": message.get('detail', {}).get('taskArn', ""), "short": False })

    fields.append({ "title": "time", "value": message['time'], "short": True})

    return {
            "color": states.get(message.get('detail', {}).get('lastStatus', ""), "danger"),
            "fallback": "ECS {} triggered".format(message['detail']),
            "fields": fields
        }

def ectwo_notification(message, region):
    fields = []
    fields.append( { "title": "account", "value": message.get('account', ""), "short": True } )
    fields.append( { "title": "region", "value": message.get('region', ""), "short": True } )
    fields.append( { "title": "time", "value": message.get('time', ""), "short": True} )

    if message.get('detail', {}).get('userIdentity',{}).get('principalId', 'NOTFOUND') != 'NOTFOUND':
      fields.append( { "title": "user", "value": message.get('detail', {}).get('userIdentity',{}).get('principalId'), "short": True } )
    if message.get('detail', {}).get('eventName', "") != "":
      fields.append( { "title": "event", "value": message.get('detail', {}).get('eventName', ""), "short": True } )
    if message.get('detail', {}).get('sourceIPAddress', "") != "":
      fields.append( { "title": "ip", "value": message.get('detail', {}).get('sourceIPAddress', ""), "short": True } )
    if message.get('detail-type', "") == 'EC2 Instance State-change Notification':
      fields.append( { "title": "state", "value": message.get('detail', {}).get('state', ""), "short": True } )
    if message.get('detail', {}).get('instance-id', "") != "":
      fields.append( { "title": "instance id", "value": message.get('detail', {}).get('instance-id', ""), "short": True } )

    return {
            "color": 'good',
            "fallback": "EC2 {} event".format(message['detail']),
            "fields": fields
        }

def deployment_notification(message, region):
    color = 'good'
    if(message.get('status', "").startswith("Error")):
        color = 'danger'
    elif(message.get('status', "").startswith("Warning")):
        color = 'warning'

    return {
            "color": color,
            "fallback": "Deployment {} event".format(message['detail']),
            "fields": [
                { "title": "account", "value": message.get('account', ""), "short": True },
                { "title": "version", "value": message.get('detail', {}).get('version', ""), "short": True },
                { "title": "region", "value": message.get('region', ""), "short": True },
                { "title": "user", "value": message.get('detail', {}).get('userIdentity',{}).get('principalId'), "short": True },
                { "title": "requested from", "value": message.get('detail', {}).get('sourceIPAddress', ""), "short": True },
                { "title": "time", "value": message['time'], "short": True}
            ]
        }

def rds_notification(message, region):
    return {
            "color": 'good',
            "fallback": "RDS {} event".format(message['detail']),
            "fields": [
                { "title": "account", "value": message.get('account', ""), "short": True },
                { "title": "region", "value": message.get('region', ""), "short": True },
                { "title": "resources", "value": message['resources'][0], "short": False },
                { "title": "message", "value": message.get('detail', {}).get('Message', ""), "short": True },
                { "title": "time", "value": message['time'], "short": True}
            ]
        }

def rds_event_subscription_notification(message, region):
    account = message.get("Source ARN").split(":")[4]
    region = message.get("Source ARN").split(":")[3]
    return {
            "color": 'good',
            "fallback": "RDS {} event".format(message['Event Message']),
            "fields": [
                { "title": "account", "value": account, "short": True },
                { "title": "region", "value": region, "short": True },
                { "title": "resources", "value": message.get('Source ID', ""), "short": False },
                { "title": "message", "value": message.get('Event Message', ""), "short": True },
                { "title": "time", "value": message['Event Time'], "short": True}
            ]
        }

def glue_notification(message, region):
    state = 'danger' if message.get('detail', {}).get('state', "") in ['FAILED', 'TIMEOUT'] else 'good'
    fields = []
    fields.append( { "title": "account", "value": message.get('account', ""), "short": True } )
    if message.get('detail', {}).get('jobName', "") != "":
      fields.append( { "title": "job", "value": message.get('detail', {}).get('jobName', ""), "short": True } )
      fields.append( { "title": "job run", "value": message.get('detail', {}).get('jobRunId', ""), "short": True } )
    if message.get('detail', {}).get('state', "") != "":
      fields.append( { "title": "state", "value": message.get('detail', {}).get('state', ""), "short": True } )
    if message.get('detail', {}).get('message', "") != "":
      fields.append( { "title": "message", "value": message.get('detail', {}).get('message', ""), "short": True } )
    return {
        "color": state,
        "fallback": "Glue {} event".format(message['detail']),
        "fields": fields
    }

def dms_notification(message, region):

    state = 'danger' if message.get('detail', {}).get('eventType', "") in ['REPLICATION_TASK_STOPPED'] else 'good'
    fields = []
    fields.append( { "title": "account", "value": message.get('account', ""), "short": True } )
    fields.append( { "title": "message", "value": message.get('detail', {}).get('detailMessage', ""), "short": True } )
    fields.append( { "title": "category", "value": message.get('detail', {}).get('category', ""), "short": True } )
    if message.get('detail', {}).get('type', "") == 'REPLICATION_TASK':
      fields.append( { "title": "task arn", "value": message.get('resources', [])[0], "short": True } )
    if message.get('detail', {}).get('resourceLink', "") != "":
      fields.append( { "title": "link", "value": '<{}|resource link>'.format(message.get('detail', {}).get('resourceLink', "")), "short": True } )
    return {
        "color": state,
        "fallback": "DMS {} event".format(message['detail']),
        "fields": fields
    }

def iam_notification(message, region):
    return {
            "color": 'good',
            "fallback": "IAM {} event".format(message['detail']),
            "fields": [
                { "title": "account", "value": message.get('account', ""), "short": True },
                { "title": "region", "value": message.get('region', ""), "short": True },
                { "title": "user", "value": message.get('detail', {}).get('userIdentity',{}).get('principalId'), "short": True },
                { "title": "message", "value": message.get('detail', {}).get('eventName', ""), "short": True },
                { "title": "ip", "value": message.get('detail', {}).get('sourceIPAddress', ""), "short": True },
                { "title": "time", "value": message['time'], "short": True}
            ]
        }


def iot_notification(message, region):
  fields = []
  if message.get("account", 'NOTFOUND') != 'NOTFOUND':
    fields.append( { "title": "account", "value": message.get('account', ""), "short": True })

  if message.get("detail", {}).get('eventName', 'NOTFOUND') != 'NOTFOUND':
    fields.append( { "title": "name", "value": message.get('detail', {}).get('eventName', ""), "short": True })

  if message.get("detail", {}).get('requestParameters', {}).get('parameters', {}).get('AWS::IoT::Certificate::CommonName', "NOTFOUND") != 'NOTFOUND':
    fields.append( { "title": "name", "CommonName": message.get("detail", {}).get('requestParameters', {}).get('parameters', {}).get('AWS::IoT::Certificate::CommonName', ""), "short": True })

  if message.get("detail", {}).get('requestParameters', {}).get('requestParameters', {}).get('thingName', "NOTFOUND") != 'NOTFOUND':
    fields.append( { "title": "ThingName", "CommonName": message.get("detail", {}).get('requestParameters', {}).get('requestParameters', {}).get('thingName', "NOTFOUND"), "short": True })

  fields.append({ "title": "time", "value": message['time'], "short": True})

  return {
    "color": 'good',
    "fallback": "IoT {} event ".format(message['detail']),
    "fields": fields
  }

def security_hub_notification(message, region):
  for finding in message.get('detail', {}).get('findings', []):
    title = finding['Title']
    status = finding['Compliance'].get('Status', "")
    product = finding['ProductName']
    severity = finding['Severity'].get('Label', "")
    state = finding['RecordState']
    resource = finding['ProductFields'].get('Resources:0/Id', "")

  return {
    "color": 'danger',
    "fallback": "{} event".format(message['detail']),
    "fields": [
      { "title": "Title", "value": title, "short": True },
      { "title": "Standard", "value": message['resources'][0], "short": True },
      { "title": "Severity", "value": severity, "short": True },
      { "title": "Region", "value": message['region'], "short": True },
      { "title": "Account", "value": message.get('account', ""), "short": True },
      { "title": "Status", "value": status, "short": True },
      { "title": "State", "value": state, "short": True },
      { "title": "Product", "value": product, "short": True },
      { "title": "Resource", "value": resource, "short": True }
    ]
  }

def systems_manager(message, region):
  return {
    "color": 'good',
    "fallback": "SSM Session Manager {} event".format(message['detail']),
    "fields": [
      { "title": "account", "value": message.get('account', ""), "short": True },
      { "title": "region", "value": message.get('region', ""), "short": True },
      { "title": "user", "value": message.get('detail', {}).get('userIdentity',{}).get('arn', ""), "short": True },
      { "title": "message", "value": message.get('detail', {}).get('eventName', ""), "short": True },
      { "title": "sessionId", "value": message.get('detail', {}).get('responseElements', {}).get('sessionId', ""), "short": True },
      { "title": "instance", "value": message.get('detail', {}).get('requestParameters', {}).get('target', ""), "short": True },
      { "title": "time", "value": message['time'], "short": True}
    ]
  }

def default_notification(subject, message):
    return {
            "fallback": "A new message",
            "fields": [{"title": subject if subject else "Message", "value": json.dumps(message), "short": False}]
        }

def filter_message_from_slack(message):
    if message.get('source', "") == "aws.iam" and message.get('detail', {}).get('eventName', '') in ["GenerateCredentialReport", "GenerateServiceLastAccessedDetails", "CreateServiceLinkedRole"]:
      return True
    elif message.get('source', "") == "aws.ecr":
      if message.get('detail', {}).get('finding-severity-counts', {}).get('CRITICAL', 0) != 0:
        return False
      else:
        return True
    elif message.get('source', "") == "aws.rds":
      if message.get('detail', {}).get('Message', '').startswith("Snapshot succeeded"):
        return True
      elif message.get('detail', {}).get('Message', '') in ["Finished DB Instance backup", "Backing up DB instance"]:
        return True
      else:
        return False
    elif message.get('source', "") == "aws.ec2":
      if message.get('detail', {}).get('eventName', '') in ["DeleteNetworkInterface", "CreateNetworkInterface"]:
        return True
      if message.get('detail', {}).get('event', '') in ["createVolume", "deleteVolume"]:
        return True
    elif message.get('source', "") == "aws.ecs":
      if message.get('detail', {}).get('eventName', '') in ["DeregisterTaskDefinition"]:
        return True
      if message.get('detail', {}).get('desiredStatus', '') in ["STOPPED"] and message.get('detail', {}).get('stopCode', '') in ["UserInitiated"]:
        return True
      if message.get('detail', {}).get('desiredStatus', '') in ["RUNNING"] and message.get('detail', {}).get('lastStatus', '') in ["PENDING", "PROVISIONING"]:
        return True
      if re.match("Scaling activity initiated by \(deployment ecs-svc\/[0-9]+\)", message.get('detail', {}).get('stoppedReason', '')):
        return True
      for key in message['detail']['containers']:
        if 'reason' in key:
          # look for reasons before exitCodes, in some instances where container exits with reason but no exitCode and all other containers have exitCode 0, we want this alert not to get filtered.
          return False
      code = []
      for key in message['detail']['containers']:
        if 'exitCode' in key:
          code.append( {"exitCode": key['exitCode'] })
      if code:
        for key in code:
          if key['exitCode'] != 0:
            return False
          else:
            continue
        return True
    elif message.get('source', "") == "aws.iot":
      if message.get('detail', {}).get('eventName', '') in ["AttachPrincipalPolicy", "CreateTopicRule", "AttachThingPrincipal", "UpdateCertificate", "SearchIndex", "RegisterCertificate", "RegisterCertificateWithoutCA", "AttachPolicy", "CreateThing"]:
        return True
    elif message.get('Event Source', "") in ["db-instance", "db-security-group", "db-parameter-group", "db-snapshot", "db-cluster", "db-cluster-snapshot"]:
      if message.get('Event Message', '') in ["Finished DB Instance backup", "Backing up DB instance", "Automated snapshot created", "Creating automated snapshot", "Creating automated cluster snapshot", "Automated cluster snapshot created", "Creating manual cluster snapshot", "Manual cluster snapshot created", "Creating manual snapshot", "Manual snapshot created", "Deleted manual snapshot"]:
        return True
      if re.match("Finished copy of snapshot awsbackup\:.*", message.get('Event Message', '')):
        return True
      if re.match("Started copy of snapshot awsbackup\:.*", message.get('Event Message', '')):
        return True
      if re.match("Started copy of snapshot rds\:.*", message.get('Event Message', '')):
        return True
      if re.match("Finished copy of snapshot rds\:.*", message.get('Event Message', '')):
        return True
      if re.match("The log file .* will be deleted since it is past the log retention period and may not be uploaded to CloudWatch Logs", message.get('Event Message', '')):
        return True
    else:
      return False

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

    if "source" in message and filter_message_from_slack(message):
        print("filtering message, not posting to slack")
        print(message)
        return

    if "Event Source" in message and filter_message_from_slack(message):
        print("filtering message, not posting to slack")
        print(message)
        return

    # pprint.pprint(message)
    if "AlarmName" in message:
        notification = cloudwatch_notification(message, region)
        payload['text'] = "AWS CloudWatch notification - " + message['AlarmName']
        payload['attachments'].append(notification)
    elif "source" in message:
        if (message['source'] == "aws.ecs"):
            notification = ecs_notification(message, region)
            payload['text'] = "AWS ECS notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "aws.ecr"):
            notification = ecr_notification(message, region)
            payload['text'] = "AWS ECR notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "aws.inspector2"):
            notification = inspector_notification(message, region)
            payload['text'] = "AWS Inspector notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "aws.ec2"):
            notification = ectwo_notification(message, region)
            payload['text'] = "AWS EC2 notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "aws.rds"):
            notification = rds_notification(message, region)
            payload['text'] = "AWS RDS notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "aws.iam"):
            notification = iam_notification(message, region)
            payload['text'] = "AWS IAM notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "aws.dms"):
            notification = dms_notification(message, region)
            payload['text'] = "AWS DMS notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "aws.glue"):
            notification = glue_notification(message, region)
            payload['text'] = "AWS Glue notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "aws.iot"):
            notification = iot_notification(message, region)
            payload['text'] = "AWS Iot notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "deployment"):
            notification = deployment_notification(message, region)
            payload['text'] = "AWS Deployment - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "aws.ssm"):
            notification = systems_manager(message, region)
            payload['text'] = "AWS Systems Manager Notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        elif (message['source'] == "aws.securityhub"):
            notification = security_hub_notification(message, region)
            payload['text'] = "AWS Security Hub Notification - " + message["detail-type"]
            payload['attachments'].append(notification)
        else:
            payload['text'] = "AWS notification"
            payload['attachments'].append(default_notification(subject, message))
    elif ("Event Source" in message and message['Event Source'] in ["db-instance", "db-security-group", "db-parameter-group", "db-snapshot", "db-cluster", "db-cluster-snapshot"]):
        notification = rds_event_subscription_notification(message, region)
        payload['text'] = "AWS RDS notification - " + message["Event Message"]
        payload['attachments'].append(notification)
    elif "Origin" in message:
        asgstates = ['Launching', 'Terminating']
        if (message.get('AutoScalingGroupName', "") != "") and (any(state in message.get('Description', "") for state in asgstates)):
            notification = asg_notification(message, region)
            event_type = ""
            if ("Terminating" in message.get('Description', "")):
                event_type = "terminating"
                payload['text'] = "AWS ASG notification - " + event_type
                payload['attachments'].append(notification)
            elif ("Launching" in message.get('Description', "")):
                event_type = "launching"
                payload['text'] = "AWS ASG notification - " + event_type
                payload['attachments'].append(notification)
        else:
            payload['text'] = "AWS notification"
            payload['attachments'].append(default_notification(subject, message))
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
