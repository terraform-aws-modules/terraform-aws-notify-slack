# AWS Notify Slack Terraform module

This module creates SNS topic (or use existing one) and a AWS Lambda function which sends notifications to Slack.

## Features

- [x] AWS Lambda runtime Python 3.6
- [?] Most of Slack options are customizable (channel, username, text, color)
- [x] Create new SNS topic or use existing one
- [?] Support different types of SNS messages:
  - [x] AWS Cloudwatch
  - ...

## Usage

```hcl
module "notify_slack" {
  source = "terraform-aws-modules/notify-slack/aws"
  
  sns_topic_name = "slack-topic"

  slack_webhook_url = "AQICAHieXmoAMw0GVceKcK11YxgXwCal77z8pCQCb3rWKNW1WAGtQtpiNegfYnxfHxq5wcebAAAAjzCBjAYJKoZIhvcNAQcGoH8wfQIBADB4BgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDC82t/I0vVFYXj+PhAIBEIBLEaSEogwZyj6VlndJZpKI2eMmV/0xLY8YqpNfys/EkC/LGxiw2mxugxXJv3oqZ4DidLwcQmcN09aNC+gPaP2XalBJCnttiDI5nhA5"

  slack_channel = "aws-notification"

  kms_key_arn = "arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"
}
```

## Use existing SNS topic or create new

If you want to subscribe AWS Lambda Function created by this module to an existing SNS topic you should specify `create_sns_topic = false` as argument and specify name of existing SNS topic name in `sns_topic_name`.

## Examples

* [notify-slack-kms](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/tree/master/modules/notify-slack-simple) - Creates SNS topic which sends messages to Slack channel and show how to use KMS to encrypt Slack webhook URL.
* [notify-slack-simple](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/tree/master/modules/notify-slack-simple) - Creates SNS topic which sends messages to Slack channel.
* [cloudwatch-alerts-to-slack](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/tree/master/modules/cloudwatch-alerts-to-slack) - Send AWS Cloudwatch alerts to Slack channel.

## Authors

Module managed by [Anton Babenko](https://github.com/antonbabenko).

## License

Apache 2 Licensed. See LICENSE for full details.
