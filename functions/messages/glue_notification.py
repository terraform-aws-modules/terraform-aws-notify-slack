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
