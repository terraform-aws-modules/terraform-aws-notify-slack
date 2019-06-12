# AWS Notify Slack Terraform module

This module creates SNS topic (or use existing one) and a AWS Lambda function which sends notifications to Slack using [incoming webhooks API](https://api.slack.com/incoming-webhooks).

Start by setting up an [incoming webhook integration](https://my.slack.com/services/new/incoming-webhook/) in your Slack workspace.

## Terraform versions

Terraform 0.12. Pin module version to `~> v2.0`. Submit pull-requests to `master` branch.

Terraform 0.11. Pin module version to `~> v1.0`. Submit pull-requests to `terraform011` branch.

## Features

- [x] AWS Lambda runtime Python 3.6
- [x] Create new SNS topic or use existing one
- [x] Support plaintext and encrypted version of Slack webhook URL
- [x] Most of Slack message options are customizable
- [x] Support different types of SNS messages:
  - [x] AWS Cloudwatch
  - [ ] [Send pull-request to add support of other message types](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/pulls)

## Usage

```hcl
module "notify_slack" {
  source  = "terraform-aws-modules/notify-slack/aws"
  version = "~> 2.0"

  sns_topic_name = "slack-topic"

  slack_webhook_url = "https://hooks.slack.com/services/AAA/BBB/CCC"
  slack_channel     = "aws-notification"
  slack_username    = "reporter"
}
```

## Use existing SNS topic or create new

If you want to subscribe AWS Lambda Function created by this module to an existing SNS topic you should specify `create_sns_topic = false` as argument and specify name of existing SNS topic name in `sns_topic_name`.

## Examples

* [notify-slack-simple](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/tree/master/examples/notify-slack-simple) - Creates SNS topic which sends messages to Slack channel.
* [cloudwatch-alerts-to-slack](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/tree/master/examples/cloudwatch-alerts-to-slack) - End to end example which shows how to send AWS Cloudwatch alerts to Slack channel and use KMS to encrypt webhook URL.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| create | Whether to create all resources | string | `true` | no |
| create_sns_topic | Whether to create new SNS topic | string | `true` | no |
| kms_key_arn | ARN of the KMS key used for decrypting slack webhook url | string | `` | no |
| lambda_function_name | The name of the Lambda function to create | string | `notify_slack` | no |
| slack_channel | The name of the channel in Slack for notifications | string | - | yes |
| slack_emoji | A custom emoji that will appear on Slack messages | string | `:aws:` | no |
| slack_username | The username that will appear on Slack messages | string | - | yes |
| slack_webhook_url | The URL of Slack webhook | string | - | yes |
| sns_topic_name | The name of the SNS topic to create | string | - | yes |

## Outputs

| Name | Description |
|------|-------------|
| lambda_iam_role_arn | The ARN of the IAM role used by Lambda function |
| lambda_iam_role_name | The name of the IAM role used by Lambda function |
| notify_slack_lambda_function_arn | The ARN of the Lambda function |
| notify_slack_lambda_function_invoke_arn | The ARN to be used for invoking Lambda function from API Gateway |
| notify_slack_lambda_function_last_modified | The date Lambda function was last modified |
| notify_slack_lambda_function_name | The name of the Lambda function |
| notify_slack_lambda_function_version | Latest published version of your Lambda function |
| this_slack_topic_arn | The ARN of the SNS topic from which messages will be sent to Slack |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Authors

Module managed by [Anton Babenko](https://github.com/antonbabenko).

## License

Apache 2 Licensed. See LICENSE for full details.
