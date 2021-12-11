# -*- coding: utf-8 -*-
"""
    Notify Slack
    ------------

    Receives event payloads that are parsed and sent to Slack

"""

import json
import logging
import os
import urllib.parse
import urllib.request
from enum import Enum
from typing import Any, Dict, Optional, Union, cast
from urllib.error import HTTPError

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import SNSEvent, event_source

logger = Logger(service="notify-slack")

# Set default region if not provided
REGION = os.environ.get("AWS_REGION", "us-east-1")

# Create client so its cached/frozen between invocations
KMS_CLIENT = boto3.client("kms", region_name=REGION)

# https://awslabs.github.io/aws-lambda-powertools-python/latest/core/logger/#logging-incoming-event
LOG_EVENTS = os.environ.get("LOG_EVENTS", "False") == "True"


class AwsService(Enum):
    """AWS service supported by function"""

    cloudwatch = "cloudwatch"
    guardduty = "guardduty"


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


class CloudWatchAlarmState(Enum):
    """Maps CloudWatch notification state to Slack message format color"""

    OK = "good"
    INSUFFICIENT_DATA = "warning"
    ALARM = "danger"


def format_cloudwatch_alarm(message: Dict[str, Any], region: str) -> Dict[str, Any]:
    """Format CloudWatch alarm event into Slack message format

    :params message: SNS message body containing CloudWatch alarm event
    :region: AWS region where the event originated from
    :returns: formatted Slack message payload
    """

    cloudwatch_url = get_service_url(region=region, service="cloudwatch")
    alarm_name = message["AlarmName"]

    return {
        "color": CloudWatchAlarmState[message["NewStateValue"]].value,
        "fallback": f"Alarm {alarm_name} triggered",
        "fields": [
            {"title": "Alarm Name", "value": f"`{alarm_name}`", "short": True},
            {
                "title": "Alarm Description",
                "value": f"`{message['AlarmDescription']}`",
                "short": False,
            },
            {
                "title": "Alarm reason",
                "value": f"`{message['NewStateReason']}`",
                "short": False,
            },
            {
                "title": "Old State",
                "value": f"`{message['OldStateValue']}`",
                "short": True,
            },
            {
                "title": "Current State",
                "value": f"`{message['NewStateValue']}`",
                "short": True,
            },
            {
                "title": "Link to Alarm",
                "value": f"{cloudwatch_url}#alarm:alarmFilter=ANY;name={urllib.parse.quote(alarm_name)}",
                "short": False,
            },
        ],
        "text": f"AWS CloudWatch notification - {message['AlarmName']}",
    }


class GuardDutyFindingSeverity(Enum):
    """Maps GuardDuty finding severity to Slack message format color"""

    Low = "#777777"
    Medium = "warning"
    High = "danger"


def format_guardduty_finding(message: Dict[str, Any], region: str) -> Dict[str, Any]:
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
        "color": GuardDutyFindingSeverity[severity].value,
        "fallback": f"GuardDuty Finding: {detail.get('title')}",
        "fields": [
            {
                "title": "Description",
                "value": f"`{detail['description']}`",
                "short": False,
            },
            {
                "title": "Finding Type",
                "value": f"`{detail['type']}`",
                "short": False,
            },
            {
                "title": "First Seen",
                "value": f"`{service['eventFirstSeen']}`",
                "short": True,
            },
            {
                "title": "Last Seen",
                "value": f"`{service['eventLastSeen']}`",
                "short": True,
            },
            {"title": "Severity", "value": f"`{severity}`", "short": True},
            {
                "title": "Count",
                "value": f"`{service['count']}`",
                "short": True,
            },
            {
                "title": "Link to Finding",
                "value": f"{guardduty_url}#/findings?search=id%3D{detail['id']}",
                "short": False,
            },
        ],
        "text": f"AWS GuardDuty Finding - {detail.get('title')}",
    }


def format_default(
    message: Union[str, Dict], subject: Optional[str] = None
) -> Dict[str, Any]:
    """
    Default formatter, converting event into Slack message format

    :params message: SNS message body containing message/event
    :returns: formatted Slack message payload
    """

    attachments = {
        "fallback": "A new message",
        "text": "AWS notification",
        "title": subject if subject else "Message",
        "mrkdwn_in": ["value"],
    }
    fields = []

    if type(message) is dict:
        for k, v in message.items():
            value = f"{json.dumps(v)}" if isinstance(v, (dict, list)) else str(v)
            fields.append({"title": k, "value": f"`{value}`", "short": len(value) < 25})
    else:
        fields.append({"value": message, "short": False})

    if fields:
        attachments["fields"] = fields  # type: ignore

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
    }
    attachment = None

    if isinstance(message, str):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            logger.info("Not a structured payload, just a string message")

    message = cast(Dict[str, Any], message)

    if "AlarmName" in message:
        notification = format_cloudwatch_alarm(message=message, region=region)
        attachment = notification

    elif (
        isinstance(message, Dict) and message.get("detail-type") == "GuardDuty Finding"
    ):
        notification = format_guardduty_finding(
            message=message, region=message["region"]
        )
        attachment = notification

    elif "attachments" in message or "text" in message:
        payload = {**payload, **message}

    else:
        attachment = format_default(message=message, subject=subject)

    if attachment:
        payload["attachments"] = [attachment]  # type: ignore

    return payload


def send_slack_notification(payload: Dict[str, Any]) -> str:
    """
    Send notification payload to Slack

    :params payload: formatted Slack message payload
    :returns: response details from sending notification
    """

    slack_url = os.environ["SLACK_WEBHOOK_URL"]
    data = urllib.parse.urlencode({"payload": json.dumps(payload)}).encode("utf-8")
    req = urllib.request.Request(slack_url)

    try:
        result = urllib.request.urlopen(req, data)
        return json.dumps({"code": result.getcode(), "info": result.info().as_string()})

    except HTTPError as err:
        logger.error(err)
        return json.dumps({"code": err.getcode(), "info": err.info().as_string()})


@logger.inject_lambda_context(log_event=LOG_EVENTS)
@event_source(data_class=SNSEvent)
def lambda_handler(event: SNSEvent, context: Dict[str, Any]) -> str:
    """
    Lambda function to parse notification events and forward to Slack

    :param event: lambda expected event object
    :param context: lambda expected context object
    :returns: none
    """

    for record in event.records:
        subject = record.sns.subject
        message = record.sns.message
        region = record.sns.topic_arn.split(":")[3]

        payload = get_slack_message_payload(
            message=message, region=region, subject=subject
        )
        response = send_slack_notification(payload=payload)

    if json.loads(response)["code"] != 200:
        response_info = json.loads(response)["info"]
        logging.error(
            f"Error: received status `{response_info}` using event `{event}` and context `{context}`"
        )

    return response
