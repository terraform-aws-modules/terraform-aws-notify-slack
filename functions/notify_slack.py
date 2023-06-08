# -*- coding: utf-8 -*-
"""
    Notify Slack
    ------------

    Receives event payloads that are parsed and sent to Slack

"""

import base64
import datetime
import json
import logging
import os
import urllib.parse
import urllib.request
from enum import Enum
from typing import Any, Dict, Optional, Union, cast
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
    securityhub = "securityhub"


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
        return ""


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
            {"title": "Account ID", "value": f"`{detail['accountId']}`", "short": True},
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


class SecurityHubFindingSeverity(Enum):
    """Maps GuardDuty finding severity to Slack message format color"""

    Low = "#777777"
    Medium = "warning"
    High = "danger"
    Critical = "#ff0209"
    Informational = "#007cbc"


def format_security_hub_finding(message: Dict[str, Any], region: str) -> Dict[str, Any]:
    """
    Format Security Hub finding event into Slack message format

    :params message: SNS message body containing Security Hub finding event
    :params region: AWS region where the event originated from
    :returns: formatted Slack message payload
    """

    securityhub_url = get_service_url(region=region, service="securityhub")
    detail = message["detail"]

    for finding in detail["findings"]:
        try:
            if finding["WorkflowState"] != "NEW":
                continue
        except Exception:
            logging.exception("The WorkflowState was not found in the JSON.")

        try:
            firstSeen = finding.get("FirstObservedAt", "<unknown>")
            findingFirstSeenTimeEpoch = round(
                datetime.datetime.strptime(
                    firstSeen, "%Y-%m-%dT%H:%M:%S.%fZ"
                ).timestamp()
            )
            firstSeen = f"<!date^{findingFirstSeenTimeEpoch}^{{date}} at {{time}} | {firstSeen}>"
        except Exception as e:
            firstSeen = "<unknown>"
            logging.error(
                f"Issue reading/formatting the findingFirstSeenTimeEpoch - {e}: result"
            )
        try:
            findingTime = finding.get("UpdatedAt", "<unknown>")
            findingTimeEpoch = round(
                datetime.datetime.strptime(
                    findingTime, "%Y-%m-%dT%H:%M:%S.%fZ"
                ).timestamp()
            )
            lastSeen = (
                f"<!date^{findingTimeEpoch}^{{date}} at {{time}} | {findingTime}>"
            )
        except Exception as e:
            lastSeen = "<unknown>"
            logging.error(
                f"Issue reading/formatting the findingTimeEpoch - {e}: result"
            )

        findingDescription = finding["Description"]
        region = ", ".join(set([res["Region"] for res in finding["Resources"]]))
        resourceType = ", ".join(set([res["Type"] for res in finding["Resources"]]))
        searchUrl = security_hub_search_url(finding)
        severity_score = finding["Severity"]["Normalized"]

        if 1 <= severity_score and severity_score <= 39:
            severity = "Low"
        elif 40 <= severity_score and severity_score <= 69:
            severity = "Medium"
        elif 70 <= severity_score and severity_score <= 89:
            severity = "High"
        elif 90 <= severity_score and severity_score <= 100:
            severity = "Critical"
        else:
            severity = "Informational"

        return {
            "color": SecurityHubFindingSeverity[severity].value,
            "fallback": f"Security Hub Finding: {finding['Title']}",
            "fields": [
                {
                    "title": "Description",
                    "value": f"`{findingDescription}`",
                    "short": False,
                },
                {
                    "title": "Finding Type",
                    "value": f"`{finding['Types']}`",
                    "short": False,
                },
                {
                    "title": "First Seen",
                    "value": f"`{firstSeen}`",
                    "short": True,
                },
                {
                    "title": "Last Seen",
                    "value": f"`{lastSeen}`",
                    "short": True,
                },
                {"title": "Severity", "value": f"`{severity}`", "short": True},
                {
                    "title": "Account ID",
                    "value": f"`{finding['AwsAccountId']}`",
                    "short": True,
                },
                {
                    "title": "Resource Type",
                    "value": f"`{resourceType}`",
                    "short": True,
                },
                {
                    "title": "Link to Finding",
                    "value": f"{securityhub_url}#/findings?search={searchUrl}",
                    "short": False,
                },
            ],
            "text": f"AWS Security Hub Finding - {finding['Title']}",
        }

    return {"": {}}


def security_hub_search_url(finding):
    searchUrl = ""
    urlEqualOperator = "%3D%255Coperator%255C%253AEQUALS%255C%253A"
    urlAndOperator = "%26"

    messageId = finding.get("Id", "")
    if messageId == "":
        generatorId = finding.get("GeneratorId", "")
        if generatorId != "":
            searchUrl = f"GeneratorId{urlEqualOperator}{generatorId}"
    else:
        searchUrl = f"AwsAccountId{urlEqualOperator}{finding['AwsAccountId']}{urlAndOperator}Id{urlEqualOperator}{messageId}"
    if searchUrl == "":
        messageId = ", ".join(set([res["Id"] for res in finding["Resources"]]))
        searchUrl = f"AwsAccountId{urlEqualOperator}{finding['AwsAccountId']}{urlAndOperator}Id{urlEqualOperator}{messageId}"

    return searchUrl


class AwsHealthCategory(Enum):
    """Maps AWS Health eventTypeCategory to Slack message format color

    eventTypeCategory
        The category code of the event. The possible values are issue,
        accountNotification, and scheduledChange.
    """

    accountNotification = "#777777"
    scheduledChange = "warning"
    issue = "danger"


def format_aws_health(message: Dict[str, Any], region: str) -> Dict[str, Any]:
    """
    Format AWS Health event into Slack message format

    :params message: SNS message body containing AWS Health event
    :params region: AWS region where the event originated from
    :returns: formatted Slack message payload
    """

    aws_health_url = (
        f"https://phd.aws.amazon.com/phd/home?region={region}#/dashboard/open-issues"
    )
    detail = message["detail"]
    resources = message.get("resources", "<unknown>")
    service = detail.get("service", "<unknown>")

    return {
        "color": AwsHealthCategory[detail["eventTypeCategory"]].value,
        "text": f"New AWS Health Event for {service}",
        "fallback": f"New AWS Health Event for {service}",
        "fields": [
            {"title": "Affected Service", "value": f"`{service}`", "short": True},
            {
                "title": "Affected Region",
                "value": f"`{message.get('region')}`",
                "short": True,
            },
            {
                "title": "Code",
                "value": f"`{detail.get('eventTypeCode')}`",
                "short": False,
            },
            {
                "title": "Event Description",
                "value": f"`{detail['eventDescription'][0]['latestDescription']}`",
                "short": False,
            },
            {
                "title": "Affected Resources",
                "value": f"`{', '.join(resources)}`",
                "short": False,
            },
            {
                "title": "Start Time",
                "value": f"`{detail.get('startTime', '<unknown>')}`",
                "short": True,
            },
            {
                "title": "End Time",
                "value": f"`{detail.get('endTime', '<unknown>')}`",
                "short": True,
            },
            {
                "title": "Link to Event",
                "value": f"{aws_health_url}",
                "short": False,
            },
        ],
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
            logging.info("Not a structured payload, just a string message")

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

    elif isinstance(message, Dict) and message.get("detail-type") == "AWS Health Event":
        notification = format_aws_health(message=message, region=message["region"])
        attachment = notification

    elif (
        isinstance(message, Dict)
        and message.get("detail-type") == "Security Hub Findings - Imported"
    ):
        notification = format_security_hub_finding(
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


def lambda_handler(event: Dict[str, Any], context: Dict[str, Any]) -> str:
    """
    Lambda function to parse notification events and forward to Slack

    :param event: lambda expected event object
    :param context: lambda expected context object
    :returns: none
    """
    if os.environ.get("LOG_EVENTS", "False") == "True":
        logging.info(f"Event logging enabled: `{json.dumps(event)}`")

    for record in event["Records"]:
        sns = record["Sns"]
        subject = sns["Subject"]
        message = sns["Message"]
        region = sns["TopicArn"].split(":")[3]

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
