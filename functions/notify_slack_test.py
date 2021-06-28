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
            "Records": [
                {
                    "EventSource": "aws:sns",
                    "EventVersion": "1.0",
                    "EventSubscriptionArn": "arn:aws:sns:eu-west-2:735598076380:service-updates:d29b4e2c-6840-9c4e-ceac-17128efcc337",
                    "Sns": {
                        "Type": "Notification",
                        "MessageId": "f86e3c5b-cd17-1ab8-80e9-c0776d4f1e7a",
                        "TopicArn": "arn:aws:sns:eu-west-2:735598076380:service-updates",
                        "Subject": "DMS Notification Message",
                        "Message": "{\"Event Source\": \"replication-task\", \"Event Time\": \"2019-02-12 15:45:24.091\", \"Identifier Link\": \"https://console.aws.amazon.com/dms/home?region=eu-west-2#tasks:ids=hello-world\\nSourceId: hello-world \", \"Event ID\": \"http://docs.aws.amazon.com/dms/latest/userguide/CHAP_Events.html#DMS-EVENT-0079 \", \"Event Message\": \"Replication task has stopped.\"}",
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
    ),
    (
      {
        "Records": [
          {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:eu-west-1:000000000000:my-sns:76cc1745-b910-4f5e-97bf-f5993b044420",
            "Sns": {
              "Type": "Notification",
              "MessageId": "00337b3f-0982-5cb1-9138-22799c885da9",
              "TopicArn": "arn:aws:sns:eu-west-1:000000000000:my-sns",
              "Subject": None,
              "Message": '{"version":"0","id":"ad3c3da1-148c-d5da-9a6a-79f1bc9a8a2e","detail-type":"Glue Job State Change","source":"aws.glue","account":"000000000000","time":"2021-06-18T12:34:06Z","region":"eu-west-1","resources":[],"detail":{"jobName":"test_job","severity":"ERROR","state":"FAILED","jobRunId":"jr_ca2144d747b45ad412d3c66a1b6934b6b27aa252be9a21a95c54dfaa224a1925","message":"SystemExit: 1"}}',
              "Timestamp": "2021-06-18T12:34:09.509Z",
              "SignatureVersion": "1",
              "Signature": "MN9H4+7QXISx+IqoRtsdIIXhd9cy9yIV916ajnDChJF9XaPi76zlwHb6RYRdi8MxKIEZsQ7F6DYV/4Hz6GqcQckqZpuYywwa3S1qUim4jw+HKtVvLAsQr/aZ0n2b/8gBC0wPpge3YaMJ13iliJ0G5Bs85MoCrTVG17TGsg8HqJkeKNx1mC4PyOMejXm+F3dwudPLozJ+CX6s+rMkiHVmpJjAv9N2qYgCKloG//dXQEU9LdZpGTDFEnazVR8PKjBEN9RTXNcNnAWuFrt+r0kOtiUoObtJOulPrUIQhIi8fvLto329wWzUQkB9wnvEt7QHeO9Qp8WhstQ3/ki8yiyAwA==",
              "SigningCertUrl": "https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
              "UnsubscribeUrl": "https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:r00000000000:my-sns:76cc1745-b910-4f5e-97bf-f5993b044420",
              "MessageAttributes": {},
            },
          }
        ]
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
