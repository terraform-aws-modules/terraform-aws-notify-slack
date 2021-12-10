{
    "Records": [
        {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1::ExampleTopic",
            "Sns": {
                "Type": "Notification",
                "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
                "Subject": "GuardDuty Finding",
                "Message": '{"detail-type": "GuardDuty Finding","region": "us-east-1","detail": {  "id": "sample-id-2",  "title": "SAMPLE Unprotected port on EC2 instance i-123123123 is being probed",  "severity": 9,  "description": "EC2 instance has an unprotected port which is being probed by a known malicious host.",  "type": "Recon:EC2 PortProbeUnprotectedPort",  "service": {    "eventFirstSeen": "2020-01-02T01:02:03Z",    "eventLastSeen": "2020-01-03T01:02:03Z",    "count": 1234  }}}',
                "Timestamp": "1970-01-01T00:00:00.000Z",
                "SignatureVersion": "1",
                "Signature": "EXAMPLE",
                "SigningCertUrl": "EXAMPLE",
                "UnsubscribeUrl": "EXAMPLE",
                "MessageAttributes": {},
            },
        }
    ]
}
