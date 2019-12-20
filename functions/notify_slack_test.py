#!/usr/bin/env pytest

import notify_slack
import pytest
from json import loads
from os import environ

events = (
    (
        {
            "Records": [
                {
                    "EventSource": "aws:sns",
                    "EventVersion": "1.0",
                    "EventSubscriptionArn": "arn:aws:sns:eu-west-2:735598076380:service-updates:d29b4e2c-6840-9c4e-ceac-17128efcc337",
                    "Sns": {
                        "Type": "Notification",
                        "MessageId": "f86e3c5b-cd17-1ab8-80e9-c0776d4f1e7a",
                        "TopicArn": "arn:aws:sns:eu-west-2:735598076380:service-updates",
                        "Subject": "OK: \"DBMigrationRequired\" in EU (London)",
                        "Message": "{\"AlarmName\":\"DBMigrationRequired\",\"AlarmDescription\":\"App is reporting \\\"A JPA error occurred (Unable to build EntityManagerFactory)\\\"\",\"AWSAccountId\":\"735598076380\",\"NewStateValue\":\"OK\",\"NewStateReason\":\"Threshold Crossed: 1 datapoint [1.0 (12/02/19 15:44:00)] was not less than the threshold (1.0).\",\"StateChangeTime\":\"2019-02-12T15:45:24.006+0000\",\"Region\":\"EU (London)\",\"OldStateValue\":\"ALARM\",\"Trigger\":{\"MetricName\":\"DBMigrationRequired\",\"Namespace\":\"LogMetrics\",\"StatisticType\":\"Statistic\",\"Statistic\":\"SUM\",\"Unit\":null,\"Dimensions\":[],\"Period\":60,\"EvaluationPeriods\":1,\"ComparisonOperator\":\"LessThanThreshold\",\"Threshold\":1.0,\"TreatMissingData\":\"- TreatMissingData:                    NonBreaching\",\"EvaluateLowSampleCountPercentile\":\"\"}}",
                        "Timestamp": "2019-02-12T15:45:24.091Z",
                        "SignatureVersion": "1",
                        "Signature": "WMYdVRN7ECNXMWZ0faRDD4fSfALW5MISB6O//LMd/LeSQYNQ/1eKYEE0PM1SHcH+73T/f/eVHbID/F203VZaGECQTD4LVA4B0DGAEY39LVbWdPTCHIDC6QCBV5ScGFZcROBXMe3UBWWMQAVTSWTE0eP526BFUTecaDFM4b9HMT4NEHWa4A2TA7d888JaVKKdSVNTd4bGS6Q2XFG1MOb652BRAHdARO7A6//2/47JZ5COM6LR0/V7TcOYCBZ20CRF6L5XLU46YYL3I1PNGKbEC1PIeVDVJVPcA17NfUbFXWYBX8LHfM4O7ZbGAPaGffDYLFWM6TX1Y6fQ01OSMc21OdUGV6HQR01e%==",
                        "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-7dd85a2b76adaa8dd603b7a0c9150589.pem",
                        "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:735598076380:service-updates:d29b4e2c-6840-9c4e-ceac-17128efcc337",
                        "MessageAttributes": {}
                    }
                }
            ]
        }
    ),
    (
      {
        "Records": [
          {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:eu-west-2:735598076380:service-updates:d29b4e2c-6840-9c4e-ceac-17128efcc337",
            "Sns": {
              "Type": "Notification",
              "MessageId": "f86e3c5b-cd17-1ab8-80e9-c0776d4f1e7a",
              "TopicArn": "arn:aws:sns:eu-west-2:735598076380:service-updates",
              "Subject": "All Fine",
              "Message": "This\nis\na typical multi-line\nmessage from SNS!\n\nHave a ~good~ amazing day! :)",
              "Timestamp": "2019-02-12T15:45:24.091Z",
              "SignatureVersion": "1",
              "Signature": "WMYdVRN7ECNXMWZ0faRDD4fSfALW5MISB6O//LMd/LeSQYNQ/1eKYEE0PM1SHcH+73T/f/eVHbID/F203VZaGECQTD4LVA4B0DGAEY39LVbWdPTCHIDC6QCBV5ScGFZcROBXMe3UBWWMQAVTSWTE0eP526BFUTecaDFM4b9HMT4NEHWa4A2TA7d888JaVKKdSVNTd4bGS6Q2XFG1MOb652BRAHdARO7A6//2/47JZ5COM6LR0/V7TcOYCBZ20CRF6L5XLU46YYL3I1PNGKbEC1PIeVDVJVPcA17NfUbFXWYBX8LHfM4O7ZbGAPaGffDYLFWM6TX1Y6fQ01OSMc21OdUGV6HQR01e%==",
              "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-7dd85a2b76adaa8dd603b7a0c9150589.pem",
              "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:735598076380:service-updates:d29b4e2c-6840-9c4e-ceac-17128efcc337",
              "MessageAttributes": {}
            }
          }
        ]
      }
    ),
    (
        {
            "AlarmName": "Example",
            "AlarmDescription": "Example alarm description.",
            "AWSAccountId": "000000000000",
            "NewStateValue": "ALARM",
            "NewStateReason": "Threshold Crossed",
            "StateChangeTime": "2017-01-12T16:30:42.236+0000",
            "Region": "EU - Ireland",
            "OldStateValue": "OK"
        }
    ),
    (
      {
        "AlarmType": "Unsupported alarm type",
        "AWSAccountId": "000000000000",
        "NewStateValue": "ALARM",
      }
    )
)


@pytest.fixture(scope='module', autouse=True)
def check_environment_variables():
    required_environment_variables = ("SLACK_CHANNEL", "SLACK_EMOJI", "SLACK_USERNAME", "SLACK_WEBHOOK_URL")
    missing_environment_variables = []
    for k in required_environment_variables:
        if k not in environ:
            missing_environment_variables.append(k)

    if len(missing_environment_variables) > 0:
        pytest.exit('Missing environment variables: {}'.format(", ".join(missing_environment_variables)))


@pytest.mark.parametrize("event", events)
def test_lambda_handler(event):
    if 'Records' in event:
        response = notify_slack.lambda_handler(event, 'self-context')

    else:
        response = notify_slack.notify_slack('subject', event, 'eu-west-1')

    response = loads(response)
    assert response['code'] == 200
