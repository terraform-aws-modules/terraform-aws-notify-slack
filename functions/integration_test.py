# -*- coding: utf-8 -*-
"""
    Integration Test
    ----------------

    Executes tests against live Slack webhook

"""

import os
from pprint import pprint
from typing import List

import boto3
import pytest


@pytest.mark.skip(reason="Execute with`pytest run python integration_test.py`")
def _get_files(directory: str) -> List[str]:
    """
    Helper function to get list of files under `directory`

    :params directory: directory to pull list of files from
    :returns: list of files names under directory specified
    """
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]


@pytest.mark.skip(reason="Execute with`pytest run python integration_test.py`")
def invoke_lambda_handler():
    """
    Invoke lambda handler with sample SNS messages

    Messages should arrive at the live webhook specified
    """
    lambda_client = boto3.client("lambda", region_name=REGION)

    # These are SNS messages that invoke the lambda handler;
    # the event payload is in the `message` field
    messages = _get_files(directory="./messages")

    for message in messages:
        with open(message, "r") as mfile:
            msg = mfile.read()
        response = lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType="Event",
            Payload=msg,
        )
        pprint(response)


@pytest.mark.skip(reason="Execute with`pytest run python integration_test.py`")
def publish_event_to_sns_topic():
    """
    Publish sample events to SNS topic created

    Messages should arrive at the live webhook specified
    """
    sns_client = boto3.client("sns", region_name=REGION)

    # These are event payloads that will get published
    events = _get_files(directory="./events")

    for event in events:
        with open(event, "r") as efile:
            msg = efile.read()
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=msg,
            Subject=event,
        )
        pprint(response)


if __name__ == "__main__":
    # Sourcing env vars set by `notify-slack-simple` example
    with open(".int.env", "r") as envvarfile:
        for line in envvarfile.readlines():
            (_var, _val) = line.strip().split("=")
            os.environ[_var] = _val

    # Not using .get() so it fails loudly if not set (`KeyError`)
    REGION = os.environ["REGION"]
    LAMBDA_FUNCTION_NAME = os.environ["LAMBDA_FUNCTION_NAME"]
    SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

    invoke_lambda_handler()
    publish_event_to_sns_topic()
