# -*- coding: utf-8 -*-
"""
    Slack Notification Test
    -----------------------

    Unit tests for `notify_slack.py`

"""

import ast
import os

import pytest
from aws_lambda_powertools.utilities.data_classes import SNSEvent

import notify_slack
import utilities

DIRNAME = os.path.dirname(__file__)


@pytest.fixture(autouse=True)
def mock_settings_env_vars(monkeypatch):
    monkeypatch.setenv("SLACK_CHANNEL", "slack_testing_sandbox")
    monkeypatch.setenv("SLACK_USERNAME", "notify_slack_test")
    monkeypatch.setenv("SLACK_EMOJI", ":aws:")
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/YOUR/WEBOOK/URL")


def test_sns_get_slack_message_payload_snapshots(snapshot, monkeypatch):
    """
    Compare outputs of get_slack_message_payload() with snapshots stored

    Run `pipenv run test:updatesnapshots` to update snapshot images
    """

    _dir = os.path.join(DIRNAME, "./messages")
    messages = [f for f in os.listdir(_dir) if os.path.isfile(os.path.join(_dir, f))]

    for file in messages:
        with open(os.path.join(_dir, file), "r") as ofile:
            event = SNSEvent(ast.literal_eval(ofile.read()))
            attachments = []

            for record in event.records:
                subject = record.sns.subject
                message = record.sns.message
                region = record.sns.topic_arn.split(":")[3]

                attachment = notify_slack.get_slack_message_payload(message=message, region=region, subject=subject)
                attachments.append(attachment)

            filename = os.path.basename(file)
            snapshot.assert_match(attachments, f"message_{filename}")


def test_event_get_slack_message_payload_snapshots(snapshot):
    """
    Compare outputs of get_slack_message_payload() with snapshots stored

    Run `pipenv run test:updatesnapshots` to update snapshot images
    """

    # These are just the raw events that will be converted to JSON string and
    # sent via SNS message
    _dir = os.path.join(DIRNAME, "./events")
    events = [f for f in os.listdir(_dir) if os.path.isfile(os.path.join(_dir, f))]

    for file in events:
        with open(os.path.join(_dir, file), "r") as ofile:
            event = ast.literal_eval(ofile.read())

            attachment = notify_slack.get_slack_message_payload(message=event, region="us-east-1", subject="bar")
            attachments = [attachment]

            filename = os.path.basename(file)
            snapshot.assert_match(attachments, f"event_{filename}")


def test_environment_variables_set(monkeypatch):
    """
    Should pass since environment variables are provided
    """

    text_message = os.path.join(os.path.join(DIRNAME, "./messages/text_message.json"))
    with open(text_message, "r") as efile:
        event = SNSEvent(ast.literal_eval(efile.read()))

        for record in event.records:
            subject = record.sns.subject
            message = record.sns.message
            region = record.sns.topic_arn.split(":")[3]

            notify_slack.get_slack_message_payload(message=message, region=region, subject=subject)


def test_environment_variables_missing(monkeypatch):
    """
    Should pass since environment variables are NOT provided and
    will raise a `KeyError`
    """
    monkeypatch.delenv("SLACK_CHANNEL")
    monkeypatch.delenv("SLACK_USERNAME")
    monkeypatch.delenv("SLACK_EMOJI")
    monkeypatch.delenv("SLACK_WEBHOOK_URL")

    with pytest.raises(KeyError):
        # will raise before parsing/validation
        notify_slack.get_slack_message_payload(message={}, region="foo", subject="bar")


@pytest.mark.parametrize(
    "region,service,expected",
    [
        (
            "us-east-1",
            "cloudwatch",
            "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1",
        ),
        (
            "us-gov-east-1",
            "cloudwatch",
            "https://console.amazonaws-us-gov.com/cloudwatch/home?region=us-gov-east-1",
        ),
        (
            "us-east-1",
            "guardduty",
            "https://console.aws.amazon.com/guardduty/home?region=us-east-1",
        ),
        (
            "us-gov-east-1",
            "guardduty",
            "https://console.amazonaws-us-gov.com/guardduty/home?region=us-gov-east-1",
        ),
    ],
)
def test_get_service_url(region, service, expected):
    assert utilities.get_service_url(region=region, service=service) == expected


def test_get_service_url_exception():
    """
    Should raise error since service is not defined in enum
    """
    with pytest.raises(KeyError):
        utilities.get_service_url(region="us-east-1", service="athena")
