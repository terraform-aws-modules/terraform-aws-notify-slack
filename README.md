AWS Notify Slack Terraform module [WIP]
=======================================

SNS topic and a Lambda function that sends notifications to Slack.


Usage
-----

```hcl
module "notify_slack" {
  source = "terraform-aws-modules/terraform-aws-notify-slack/aws"
  
  slack_topic_name = "slacktopic"

  slack_webhook_url = "AQICAHieXmoAMw0GVceKcK11YxgXwCal77z8pCQCb3rWKNW1WAGtQtpiNegfYnxfHxq5wcebAAAAjzCBjAYJKoZIhvcNAQcGoH8wfQIBADB4BgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDC82t/I0vVFYXj+PhAIBEIBLEaSEogwZyj6VlndJZpKI2eMmV/0xLY8YqpNfys/EkC/LGxiw2mxugxXJv3oqZ4DidLwcQmcN09aNC+gPaP2XalBJCnttiDI5nhA5"

  slack_channel = "aws-notification"

  kms_key_arn = "arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"

}
```

License
-------

Apache 2 Licensed. See LICENSE for full details.
