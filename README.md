# AWS Notify Slack Terraform module

This module creates SNS topic (or use existing one) and a AWS Lambda function which sends notifications to Slack using [incoming webhooks API](https://api.slack.com/incoming-webhooks).

Start by setting up an [incoming webhook integration](https://my.slack.com/services/new/incoming-webhook/) in your Slack workspace.

## Features

- [x] AWS Lambda runtime Python 3.6
- [?] Most of Slack options are customizable (channel, username, text, color)
- [x] Create new SNS topic or use existing one
- [x] Support plaintext and encrypted version of webhook URL
- [?] Support different types of SNS messages:
  - [x] AWS Cloudwatch
  - ...

## Usage

```hcl
module "notify_slack" {
  source = "terraform-aws-modules/notify-slack/aws"
  
  sns_topic_name = "slack-topic"

  slack_webhook_url = "https://hooks.slack.com/services/AAA/BBB/CCC"
  slack_channel     = "aws-notification"
  slack_username    = "reporter"
}
```

## Use existing SNS topic or create new

If you want to subscribe AWS Lambda Function created by this module to an existing SNS topic you should specify `create_sns_topic = false` as argument and specify name of existing SNS topic name in `sns_topic_name`.

## Examples

* [notify-slack-simple](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/tree/master/modules/notify-slack-simple) - Creates SNS topic which sends messages to Slack channel.
* [notify-slack-kms](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/tree/master/modules/notify-slack-simple) - Creates SNS topic which sends messages to Slack channel (using KMS to encrypt Slack webhook URL).
* [cloudwatch-alerts-to-slack](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/tree/master/modules/cloudwatch-alerts-to-slack) - End to end example which shows how to send AWS Cloudwatch alerts to Slack channel.

## Authors

Module managed by [Anton Babenko](https://github.com/antonbabenko).

## License

Apache 2 Licensed. See LICENSE for full details.
