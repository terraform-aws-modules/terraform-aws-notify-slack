#!/usr/bin/env pytest

import json
import os

import notify_slack
import pytest
from events.events import events


@pytest.fixture(scope="module", autouse=True)
def check_environment_variables():
    required_environment_variables = (
        "SLACK_CHANNEL",
        "SLACK_EMOJI",
        "SLACK_USERNAME",
        "SLACK_WEBHOOK_URL",
    )
    missing_environment_variables = []
    for k in required_environment_variables:
        if k not in os.environ:
            missing_environment_variables.append(k)

    if len(missing_environment_variables) > 0:
        pytest.exit(
            f"Missing environment variables: {', '.join(missing_environment_variables)}"
        )


@pytest.mark.parametrize("event", events)
def test_lambda_handler(event):
    if "Records" in event:
        response = notify_slack.lambda_handler(event, "self-context")

    else:

        payload = notify_slack.get_slack_message_payload(
            message=event, region="eu-west-1", subject="subject"
        )
        response = notify_slack.send_slack_notification(payload=payload)

    response = json.loads(response)
    assert response["code"] == 200


@pytest.mark.parametrize(
    "region,service,expected",
    [
        (
            "us-east-1",
            "cloudwatch",
            "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1",
        )
    ],
)
def test_get_service_url(region, service, expected):
    assert notify_slack.get_service_url(region=region, service=service) == expected


def test_get_service_url_exception():
    with pytest.raises(KeyError):
        notify_slack.get_service_url(region="us-east-1", service="athena")
