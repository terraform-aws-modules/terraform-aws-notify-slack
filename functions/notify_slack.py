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
from typing import Any, Dict, Optional, Union, cast
from urllib.error import HTTPError

from aws_lambda_powertools import Logger  # type: ignore
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.data_classes import SNSEvent, event_source

from cloudwatch import get_slack_attachment as get_cloudwatch_slack_attachment
from guardduty import get_slack_attachment as get_guardduty_slack_attachment

logger = Logger(service="notify-slack")

# https://awslabs.github.io/aws-lambda-powertools-python/latest/core/logger/#logging-incoming-event
LOG_EVENTS = os.environ.get("LOG_EVENTS", "False") == "True"


def format_default(message: Union[str, Dict], subject: Optional[str] = None) -> Dict[str, Any]:
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


def get_slack_message_payload(message: Union[str, Dict], region: str, subject: Optional[str] = None) -> Dict:
    """
    Parse notification message and format into Slack message payload

    :params message: SNS message body notification payload
    :params region: AWS region where the event originated from
    :params subject: Optional subject line for Slack notification
    :returns: Slack message payload
    """

    slack_username = os.environ["SLACK_USERNAME"]
    slack_emoji = os.environ["SLACK_EMOJI"]

    payload = {
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
        attachment = get_cloudwatch_slack_attachment(message=message, region=region)

    elif isinstance(message, Dict) and message.get("detail-type") == "GuardDuty Finding":
        attachment = get_guardduty_slack_attachment(message=message, region=message["region"])

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

    # Pull from SSM parameter
    webhook_url_ssm_param_name = os.environ.get("SLACK_WEBHOOK_URL_SSM_PARAM_NAME")
    if webhook_url_ssm_param_name:
        slack_webhook_url = parameters.get_parameter(webhook_url_ssm_param_name, decrypt=True, max_age=300)

    # Pull from Secrets Manager
    webhook_url_secret_name = os.environ.get("SLACK_WEBHOOK_URL_SECRET_NAME")
    if webhook_url_secret_name:
        slack_webhook_url = parameters.get_secret(webhook_url_secret_name, max_age=300)

    if not slack_webhook_url:
        raise KeyError("One of `SLACK_WEBHOOK_URL_SSM_PARAM_NAME` or `SLACK_WEBHOOK_URL_SECRET_NAME` must be provided")

    data = urllib.parse.urlencode({"payload": json.dumps(payload)}).encode("utf-8")
    req = urllib.request.Request(cast(str, slack_webhook_url))

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

        payload = get_slack_message_payload(message=message, region=region, subject=subject)
        response = send_slack_notification(payload=payload)

    if json.loads(response)["code"] != 200:
        response_info = json.loads(response)["info"]
        logging.error(f"Error: received status `{response_info}` using event `{event}` and context `{context}`")

    return response
