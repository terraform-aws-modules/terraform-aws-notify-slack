import base64
import json
import logging
import os
import urllib.parse
import urllib.request
from enum import Enum
from urllib.error import HTTPError

import boto3

# Set default region if not provided
REGION = os.environ.get("AWS_REGION", "us-east-1")

# Create client so its cached/frozen between invocations
KMS_CLIENT = boto3.client("kms", region_name=REGION)


class AwsService(Enum):
    """AWS service supported by function"""

    cloudwatch = "cloudwatch"
    guardduty = "guardduty"


def decrypt(encrypted_url: str) -> str:
    """Decrypt encrypted URL with KMS

    :param encrypted_url: URL to decrypt with KMS
    :returns: plaintext URL
    """
    try:
        decrypted_payload = KMS_CLIENT.decrypt(
            CiphertextBlob=base64.b64decode(encrypted_url)
        )
        return decrypted_payload["Plaintext"].decode()
    except Exception:
        logging.exception("Failed to decrypt URL with KMS")


def get_service_url(region: str, service: str) -> str:
    """Get the appropriate service URL for the region

    :param region: name of the AWS region
    :param service: name of the AWS service
    :returns: AWS console url formatted for the region and service provided
    """
    try:
        service_name = AwsService[service].value

        if region.startswith("us-gov-"):
            return f"https://console.amazonaws-us-gov.com/{service_name}/home?region={region}"
        else:
            return f"https://console.aws.amazon.com/{service_name}/home?region={region}"

    except KeyError:
        print(f"Service {service} is currently not supported")
        raise


def cloudwatch_notification(message, region):
    states = {"OK": "good", "INSUFFICIENT_DATA": "warning", "ALARM": "danger"}
    cloudwatch_url = get_service_url(region=region, service="cloudwatch")
    alarm_name = message["AlarmName"]
    return {
        "color": states[message["NewStateValue"]],
        "fallback": f"Alarm {alarm_name} triggered",
        "fields": [
            {"title": "Alarm Name", "value": alarm_name, "short": True},
            {
                "title": "Alarm Description",
                "value": message["AlarmDescription"],
                "short": False,
            },
            {
                "title": "Alarm reason",
                "value": message["NewStateReason"],
                "short": False,
            },
            {"title": "Old State", "value": message["OldStateValue"], "short": True},
            {
                "title": "Current State",
                "value": message["NewStateValue"],
                "short": True,
            },
            {
                "title": "Link to Alarm",
                "value": f"{cloudwatch_url}#alarm:alarmFilter=ANY;name={urllib.parse.quote(alarm_name)}",
                "short": False,
            },
        ],
    }


def guardduty_finding(message, region):
    states = {"Low": "#777777", "Medium": "warning", "High": "danger"}
    guardduty_url = get_service_url(region=region, service="guardduty")

    detail = message["details"]
    severity_score = detail.get("severity")

    if severity_score < 4.0:
        severity = "Low"
    elif severity_score < 7.0:
        severity = "Medium"
    else:
        severity = "High"

    service = detail.get("service", {})

    return {
        "color": states[severity],
        "fallback": f"GuardDuty Finding: {detail.get('title')}",
        "fields": [
            {
                "title": "Description",
                "value": detail.get("description"),
                "short": False,
            },
            {
                "title": "Finding type",
                "value": detail.get("type"),
                "short": False,
            },
            {
                "title": "First Seen",
                "value": service.get("eventFirstSeen"),
                "short": True,
            },
            {
                "title": "Last Seen",
                "value": service.get("eventLastSeen"),
                "short": True,
            },
            {"title": "Severity", "value": severity, "short": True},
            {
                "title": "Count",
                "value": service.get("count"),
                "short": True,
            },
            {
                "title": "Link to Finding",
                "value": f"{guardduty_url}#/findings?search=id%3D{detail.get('id')}",
                "short": False,
            },
        ],
    }


def default_notification(subject, message):
    attachments = {
        "fallback": "A new message",
        "title": subject if subject else "Message",
        "mrkdwn_in": ["value"],
        "fields": [],
    }
    if type(message) is dict:
        for k, v in message.items():
            value = f"`{json.dumps(v)}`" if isinstance(v, (dict, list)) else str(v)
            attachments["fields"].append(
                {"title": k, "value": value, "short": len(value) < 25}
            )
    else:
        attachments["fields"].append({"value": message, "short": False})

    return attachments


# Send a message to a slack channel
def notify_slack(subject, message, region):
    slack_url = os.environ["SLACK_WEBHOOK_URL"]
    if not slack_url.startswith("http"):
        slack_url = decrypt(slack_url)

    slack_channel = os.environ["SLACK_CHANNEL"]
    slack_username = os.environ["SLACK_USERNAME"]
    slack_emoji = os.environ["SLACK_EMOJI"]

    payload = {
        "channel": slack_channel,
        "username": slack_username,
        "icon_emoji": slack_emoji,
        "attachments": [],
    }

    if type(message) is str:
        try:
            message = json.loads(message)
        except json.JSONDecodeError as err:
            logging.exception(f"JSON decode error: {err}")

    if "AlarmName" in message:
        notification = cloudwatch_notification(message, region)
        payload["text"] = f"AWS CloudWatch notification - {message['AlarmName']}"
        payload["attachments"].append(notification)
    elif "detail-type" in message and message["detail-type"] == "GuardDuty Finding":
        notification = guardduty_finding(message, message["region"])
        payload["text"] = f"Amazon GuardDuty Finding - {message['detail']['title']}"
        payload["attachments"].append(notification)
    elif "attachments" in message or "text" in message:
        payload = {**payload, **message}
    else:
        payload["text"] = "AWS notification"
        payload["attachments"].append(default_notification(subject, message))

    data = urllib.parse.urlencode({"payload": json.dumps(payload)}).encode("utf-8")
    req = urllib.request.Request(slack_url)

    try:
        result = urllib.request.urlopen(req, data)
        return json.dumps({"code": result.getcode(), "info": result.info().as_string()})

    except HTTPError as e:
        logging.error(f"{e}: result")
        return json.dumps({"code": e.getcode(), "info": e.info().as_string()})


def lambda_handler(event, context):
    if "LOG_EVENTS" in os.environ and os.environ["LOG_EVENTS"] == "True":
        logging.warning(f"Event logging enabled: `{json.dumps(event)}`")

    sns_record = event["Records"][0]["Sns"]

    subject = sns_record["Subject"]
    message = sns_record["Message"]
    region = sns_record["TopicArn"].split(":")[3]
    response = notify_slack(subject, message, region)

    if json.loads(response)["code"] != 200:
        response_info = json.loads(response)["info"]
        logging.error(
            f"Error: received status `{response_info}` using event `{event}` and context `{context}`"
        )

    return response
