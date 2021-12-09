import base64
import json
import logging
import os
import urllib.parse
import urllib.request
from enum import Enum
from typing import Dict, Optional, Union
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


def decrypt_url(encrypted_url: str) -> str:
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


class CloudWatchStateColor(Enum):
    """Maps CloudWatch notification state to Slack message format color"""

    OK = "good"
    INSUFFICIENT_DATA = "warning"
    ALARM = "danger"


def format_cloudwatch_notification(message: Dict, region: str) -> Dict:
    """Format CloudWatch event notification into Slack message format

    :params message: SNS message body containing CloudWatch notification event
    :region: AWS region where the event originated from
    :returns: formatted Slack message payload
    """

    cloudwatch_url = get_service_url(region=region, service="cloudwatch")
    alarm_name = message["AlarmName"]

    return {
        "color": CloudWatchStateColor[message["NewStateValue"]].value,
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


class GuardDutySeverityColor(Enum):
    """Maps GuardDuty finding severity to Slack message format color"""

    Low = "#777777"
    Medium = "warning"
    High = "danger"


def format_guardduty_finding(message: Dict, region: str) -> Dict:
    """
    Format GuardDuty finding event into Slack message format

    :params message: SNS message body containing GuardDuty finding event
    :params region: AWS region where the event originated from
    :returns: formatted Slack message payload
    """

    guardduty_url = get_service_url(region=region, service="guardduty")
    detail = message["detail"]
    service = detail.get("service", {})
    severity_score = detail.get("severity")

    if severity_score < 4.0:
        severity = "Low"
    elif severity_score < 7.0:
        severity = "Medium"
    else:
        severity = "High"

    return {
        "color": GuardDutySeverityColor[severity].value,
        "fallback": f"GuardDuty Finding: {detail.get('title')}",
        "fields": [
            {
                "title": "Description",
                "value": detail.get("description"),
                "short": False,
            },
            {
                "title": "Finding Type",
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


def format_default_notification(
    message: Union[str, Dict], subject: Optional[str] = None
) -> Dict:
    """
    Format default, general notification into Slack message format

    :params message: SNS message body containing message/notification event
    :returns: formatted Slack message payload
    """

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


def get_slack_message_payload(
    message: Union[str, Dict], region: str, subject: Optional[str] = None
) -> Dict:
    """
    Parse notification message and format into Slack message payload

    :params message: SNS message body notification payload
    :params region: AWS region where the event originated from
    :params subject: Optional subject line for Slack notification
    :returns: Slack message payload
    """

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
        notification = format_cloudwatch_notification(message, region)
        payload["text"] = f"AWS CloudWatch notification - {message['AlarmName']}"
        payload["attachments"].append(notification)

    elif "detail-type" in message and message["detail-type"] == "GuardDuty Finding":
        notification = format_guardduty_finding(message, message["region"])
        payload["text"] = f"Amazon GuardDuty Finding - {message['detail']['title']}"
        payload["attachments"].append(notification)

    elif "attachments" in message or "text" in message:
        payload = {**payload, **message}

    else:
        payload["text"] = "AWS notification"
        payload["attachments"].append(
            format_default_notification(message=message, subject=subject)
        )

    return payload


def send_slack_notification(payload: Dict) -> Dict:
    """
    Send notification payload to Slack

    :params payload: formatted Slack message paylod
    :returns: response details from sending notification
    """

    slack_url = os.environ["SLACK_WEBHOOK_URL"]
    if not slack_url.startswith("http"):
        slack_url = decrypt_url(slack_url)

    data = urllib.parse.urlencode({"payload": json.dumps(payload)}).encode("utf-8")
    req = urllib.request.Request(slack_url)

    try:
        result = urllib.request.urlopen(req, data)
        return json.dumps({"code": result.getcode(), "info": result.info().as_string()})

    except HTTPError as e:
        logging.error(f"{e}: result")
        return json.dumps({"code": e.getcode(), "info": e.info().as_string()})


def lambda_handler(event: Dict, context: Dict) -> Dict:
    """
    Lambda function to parse notification events and forward to Slack

    :param event: lambda expected event object
    :param context: lambda expected context object
    :returns: none
    """
    if os.environ.get("LOG_EVENTS", "False") == "True":
        logging.info(f"Event logging enabled: `{json.dumps(event)}`")

    sns_record = event["Records"][0]["Sns"]

    subject = sns_record["Subject"]
    message = sns_record["Message"]
    region = sns_record["TopicArn"].split(":")[3]

    payload = get_slack_message_payload(message=message, region=region, subject=subject)
    response = send_slack_notification(payload=payload)

    if json.loads(response)["code"] != 200:
        response_info = json.loads(response)["info"]
        logging.error(
            f"Error: received status `{response_info}` using event `{event}` and context `{context}`"
        )

    return response
