# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['test_event_get_slack_message_payload_snapshots event_cloudwatch_alarm.json'] = [
    {
        'attachments': [
            {
                'color': 'danger',
                'fallback': 'Alarm Example triggered',
                'fields': [
                    {
                        'short': True,
                        'title': 'Alarm Name',
                        'value': '`Example`'
                    },
                    {
                        'short': False,
                        'title': 'Alarm Description',
                        'value': '`Example alarm description.`'
                    },
                    {
                        'short': False,
                        'title': 'Alarm reason',
                        'value': '`Threshold Crossed`'
                    },
                    {
                        'short': True,
                        'title': 'Old State',
                        'value': '`OK`'
                    },
                    {
                        'short': True,
                        'title': 'Current State',
                        'value': '`ALARM`'
                    },
                    {
                        'short': False,
                        'title': 'Link to Alarm',
                        'value': 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#alarm:alarmFilter=ANY;name=Example'
                    }
                ],
                'text': 'AWS CloudWatch notification - Example'
            }
        ],
        'icon_emoji': ':aws:',
        'username': 'notify_slack_test'
    }
]

snapshots['test_event_get_slack_message_payload_snapshots event_guardduty_finding_high.json'] = [
    {
        'attachments': [
            {
                'color': 'danger',
                'fallback': 'GuardDuty Finding: SAMPLE Unprotected port on EC2 instance i-123123123 is being probed',
                'fields': [
                    {
                        'short': False,
                        'title': 'Description',
                        'value': '`EC2 instance has an unprotected port which is being probed by a known malicious host.`'
                    },
                    {
                        'short': False,
                        'title': 'Finding Type',
                        'value': '`Recon:EC2 PortProbeUnprotectedPort`'
                    },
                    {
                        'short': True,
                        'title': 'First Seen',
                        'value': '`2020-01-02T01:02:03Z`'
                    },
                    {
                        'short': True,
                        'title': 'Last Seen',
                        'value': '`2020-01-03T01:02:03Z`'
                    },
                    {
                        'short': True,
                        'title': 'Severity',
                        'value': '`High`'
                    },
                    {
                        'short': True,
                        'title': 'Count',
                        'value': '`1234`'
                    },
                    {
                        'short': False,
                        'title': 'Link to Finding',
                        'value': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1#/findings?search=id%3Dsample-id-2'
                    }
                ],
                'text': 'AWS GuardDuty Finding - SAMPLE Unprotected port on EC2 instance i-123123123 is being probed'
            }
        ],
        'icon_emoji': ':aws:',
        'username': 'notify_slack_test'
    }
]

snapshots['test_event_get_slack_message_payload_snapshots event_guardduty_finding_low.json'] = [
    {
        'attachments': [
            {
                'color': '#777777',
                'fallback': 'GuardDuty Finding: SAMPLE Unprotected port on EC2 instance i-123123123 is being probed',
                'fields': [
                    {
                        'short': False,
                        'title': 'Description',
                        'value': '`EC2 instance has an unprotected port which is being probed by a known malicious host.`'
                    },
                    {
                        'short': False,
                        'title': 'Finding Type',
                        'value': '`Recon:EC2 PortProbeUnprotectedPort`'
                    },
                    {
                        'short': True,
                        'title': 'First Seen',
                        'value': '`2020-01-02T01:02:03Z`'
                    },
                    {
                        'short': True,
                        'title': 'Last Seen',
                        'value': '`2020-01-03T01:02:03Z`'
                    },
                    {
                        'short': True,
                        'title': 'Severity',
                        'value': '`Low`'
                    },
                    {
                        'short': True,
                        'title': 'Count',
                        'value': '`1234`'
                    },
                    {
                        'short': False,
                        'title': 'Link to Finding',
                        'value': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1#/findings?search=id%3Dsample-id-2'
                    }
                ],
                'text': 'AWS GuardDuty Finding - SAMPLE Unprotected port on EC2 instance i-123123123 is being probed'
            }
        ],
        'icon_emoji': ':aws:',
        'username': 'notify_slack_test'
    }
]

snapshots['test_event_get_slack_message_payload_snapshots event_guardduty_finding_medium.json'] = [
    {
        'attachments': [
            {
                'color': 'warning',
                'fallback': 'GuardDuty Finding: SAMPLE Unprotected port on EC2 instance i-123123123 is being probed',
                'fields': [
                    {
                        'short': False,
                        'title': 'Description',
                        'value': '`EC2 instance has an unprotected port which is being probed by a known malicious host.`'
                    },
                    {
                        'short': False,
                        'title': 'Finding Type',
                        'value': '`Recon:EC2 PortProbeUnprotectedPort`'
                    },
                    {
                        'short': True,
                        'title': 'First Seen',
                        'value': '`2020-01-02T01:02:03Z`'
                    },
                    {
                        'short': True,
                        'title': 'Last Seen',
                        'value': '`2020-01-03T01:02:03Z`'
                    },
                    {
                        'short': True,
                        'title': 'Severity',
                        'value': '`Medium`'
                    },
                    {
                        'short': True,
                        'title': 'Count',
                        'value': '`1234`'
                    },
                    {
                        'short': False,
                        'title': 'Link to Finding',
                        'value': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1#/findings?search=id%3Dsample-id-2'
                    }
                ],
                'text': 'AWS GuardDuty Finding - SAMPLE Unprotected port on EC2 instance i-123123123 is being probed'
            }
        ],
        'icon_emoji': ':aws:',
        'username': 'notify_slack_test'
    }
]

snapshots['test_sns_get_slack_message_payload_snapshots message_cloudwatch_alarm.json'] = [
    {
        'attachments': [
            {
                'color': 'good',
                'fallback': 'Alarm DBMigrationRequired triggered',
                'fields': [
                    {
                        'short': True,
                        'title': 'Alarm Name',
                        'value': '`DBMigrationRequired`'
                    },
                    {
                        'short': False,
                        'title': 'Alarm Description',
                        'value': '`App is reporting "A JPA error occurred(Unable to build EntityManagerFactory)"`'
                    },
                    {
                        'short': False,
                        'title': 'Alarm reason',
                        'value': '`Threshold Crossed: 1 datapoint [1.0 (12/02/19 15:44:00)] was not less than the threshold (1.0).`'
                    },
                    {
                        'short': True,
                        'title': 'Old State',
                        'value': '`ALARM`'
                    },
                    {
                        'short': True,
                        'title': 'Current State',
                        'value': '`OK`'
                    },
                    {
                        'short': False,
                        'title': 'Link to Alarm',
                        'value': 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#alarm:alarmFilter=ANY;name=DBMigrationRequired'
                    }
                ],
                'text': 'AWS CloudWatch notification - DBMigrationRequired'
            }
        ],
        'icon_emoji': ':aws:',
        'username': 'notify_slack_test'
    }
]

snapshots['test_sns_get_slack_message_payload_snapshots message_dms_notification.json'] = [
    {
        'attachments': [
            {
                'fallback': 'A new message',
                'fields': [
                    {
                        'short': True,
                        'title': 'Event Source',
                        'value': '`replication-task`'
                    },
                    {
                        'short': True,
                        'title': 'Event Time',
                        'value': '`2019-02-12 15:45:24.091`'
                    },
                    {
                        'short': False,
                        'title': 'Identifier Link',
                        'value': '`https://console.aws.amazon.com/dms/home?region=us-east-1#tasks:ids=hello-world`'
                    },
                    {
                        'short': True,
                        'title': 'SourceId',
                        'value': '`hello-world`'
                    },
                    {
                        'short': False,
                        'title': 'Event ID',
                        'value': '`http://docs.aws.amazon.com/dms/latest/userguide/CHAP_Events.html#DMS-EVENT-0079 `'
                    },
                    {
                        'short': False,
                        'title': 'Event Message',
                        'value': '`Replication task has stopped.`'
                    }
                ],
                'mrkdwn_in': [
                    'value'
                ],
                'text': 'AWS notification',
                'title': 'DMS Notification Message'
            }
        ],
        'icon_emoji': ':aws:',
        'username': 'notify_slack_test'
    }
]

snapshots['test_sns_get_slack_message_payload_snapshots message_glue_notification.json'] = [
    {
        'attachments': [
            {
                'fallback': 'A new message',
                'fields': [
                    {
                        'short': True,
                        'title': 'version',
                        'value': '`0`'
                    },
                    {
                        'short': False,
                        'title': 'id',
                        'value': '`ad3c3da1-148c-d5da-9a6a-79f1bc9a8a2e`'
                    },
                    {
                        'short': True,
                        'title': 'detail-type',
                        'value': '`Glue Job State Change`'
                    },
                    {
                        'short': True,
                        'title': 'source',
                        'value': '`aws.glue`'
                    },
                    {
                        'short': True,
                        'title': 'account',
                        'value': '`000000000000`'
                    },
                    {
                        'short': True,
                        'title': 'time',
                        'value': '`2021-06-18T12:34:06Z`'
                    },
                    {
                        'short': True,
                        'title': 'region',
                        'value': '`us-east-2`'
                    },
                    {
                        'short': True,
                        'title': 'resources',
                        'value': '`[]`'
                    },
                    {
                        'short': False,
                        'title': 'detail',
                        'value': '`{"jobName": "test_job", "severity": "ERROR", "state": "FAILED", "jobRunId": "jr_ca2144d747b45ad412d3c66a1b6934b6b27aa252be9a21a95c54dfaa224a1925", "message": "SystemExit: 1"}`'
                    }
                ],
                'mrkdwn_in': [
                    'value'
                ],
                'text': 'AWS notification',
                'title': 'Message'
            }
        ],
        'icon_emoji': ':aws:',
        'username': 'notify_slack_test'
    }
]

snapshots['test_sns_get_slack_message_payload_snapshots message_guardduty_finding.json'] = [
    {
        'attachments': [
            {
                'color': 'danger',
                'fallback': 'GuardDuty Finding: SAMPLE Unprotected port on EC2 instance i-123123123 is being probed',
                'fields': [
                    {
                        'short': False,
                        'title': 'Description',
                        'value': '`EC2 instance has an unprotected port which is being probed by a known malicious host.`'
                    },
                    {
                        'short': False,
                        'title': 'Finding Type',
                        'value': '`Recon:EC2 PortProbeUnprotectedPort`'
                    },
                    {
                        'short': True,
                        'title': 'First Seen',
                        'value': '`2020-01-02T01:02:03Z`'
                    },
                    {
                        'short': True,
                        'title': 'Last Seen',
                        'value': '`2020-01-03T01:02:03Z`'
                    },
                    {
                        'short': True,
                        'title': 'Severity',
                        'value': '`High`'
                    },
                    {
                        'short': True,
                        'title': 'Count',
                        'value': '`1234`'
                    },
                    {
                        'short': False,
                        'title': 'Link to Finding',
                        'value': 'https://console.amazonaws-us-gov.com/guardduty/home?region=us-gov-east-1#/findings?search=id%3Dsample-id-2'
                    }
                ],
                'text': 'AWS GuardDuty Finding - SAMPLE Unprotected port on EC2 instance i-123123123 is being probed'
            }
        ],
        'icon_emoji': ':aws:',
        'username': 'notify_slack_test'
    }
]

snapshots['test_sns_get_slack_message_payload_snapshots message_text_message.json'] = [
    {
        'attachments': [
            {
                'fallback': 'A new message',
                'fields': [
                    {
                        'short': False,
                        'value': '''This
is
a typical multi-line
message from SNS!

Have a ~good~ amazing day! :)'''
                    }
                ],
                'mrkdwn_in': [
                    'value'
                ],
                'text': 'AWS notification',
                'title': 'All Fine'
            }
        ],
        'icon_emoji': ':aws:',
        'username': 'notify_slack_test'
    }
]
