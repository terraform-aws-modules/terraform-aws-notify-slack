# -*- coding: utf-8 -*-
"""
    CloudWatch
    ----------

    Handles validation, parsing, and formatting of CloudWatch events

"""

import urllib
from enum import Enum
from typing import Any, Dict

from utilities import get_service_url


class CloudWatchAlarmState(Enum):
    """Maps CloudWatch notification state to Slack message format color"""

    OK = "good"
    INSUFFICIENT_DATA = "warning"
    ALARM = "danger"


def get_slack_attachment(message: Dict[str, Any], region: str) -> Dict[str, Any]:
    """Format CloudWatch alarm event into Slack message attachment

    :params message: SNS message body containing CloudWatch alarm event
    :region: AWS region where the event originated from
    :returns: formatted Slack message attachment
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
