# -*- coding: utf-8 -*-
"""
    Slack Notification Test
    -----------------------

    Unit tests for `notify_slack.py`

"""

import ast
import os

import notify_slack
import pytest


def test_get_slack_message_payload_snapshots(snapshot, monkeypatch):
    """
    Compare outputs of get_slack_message_payload() with snapshots stored

    Run `pipenv run test:updatesnapshots` to update snapshot images
    """

    monkeypatch.setenv("SLACK_CHANNEL", "slack_testing_sandbox")
    monkeypatch.setenv("SLACK_USERNAME", "notify_slack_test")
    monkeypatch.setenv("SLACK_EMOJI", ":aws:")

    _dir = "./events"
    event_files = [f for f in os.listdir(_dir) if os.path.isfile(os.path.join(_dir, f))]

    for file in event_files:
        with open(os.path.join(_dir, file), "r") as efile:
            event = ast.literal_eval(efile.read())

            attachments = []
            for record in event["Records"]:
                sns = record["Sns"]
                subject = sns["Subject"]
                message = sns["Message"]
                region = sns["TopicArn"].split(":")[3]

                attachment = notify_slack.get_slack_message_payload(
                    message=message, region=region, subject=subject
                )
                attachments.append(attachment)

            filename = os.path.basename(file)
            snapshot.assert_match(attachments, filename)


def test_environment_variables_set(monkeypatch):
    """
    Should pass since environment variables are provided
    """

    monkeypatch.setenv("SLACK_CHANNEL", "slack_testing_sandbox")
    monkeypatch.setenv("SLACK_USERNAME", "notify_slack_test")
    monkeypatch.setenv("SLACK_EMOJI", ":aws:")
    monkeypatch.setenv(
        "SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/YOUR/WEBOOK/URL"
    )

    with open(os.path.join("./events/sns_message.py"), "r") as efile:
        event = ast.literal_eval(efile.read())

        for record in event["Records"]:
            sns = record["Sns"]
            subject = sns["Subject"]
            message = sns["Message"]
            region = sns["TopicArn"].split(":")[3]

            notify_slack.get_slack_message_payload(
                message=message, region=region, subject=subject
            )


def test_environment_variables_missing():
    """
    Should pass since environment variables are NOT provided and
    will raise a `KeyError`
    """
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
    assert notify_slack.get_service_url(region=region, service=service) == expected


def test_get_service_url_exception():
    """
    Should raise error since service is not defined in enum
    """
    with pytest.raises(KeyError):
        notify_slack.get_service_url(region="us-east-1", service="athena")
