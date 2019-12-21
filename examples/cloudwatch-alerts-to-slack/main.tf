provider "aws" {
  region = "eu-west-1"
}

resource "aws_kms_key" "this" {
  description = "KMS key for notify-slack test"
}

# Encrypt the URL, storing encryption here will show it in logs and in tfstate
# https://www.terraform.io/docs/state/sensitive-data.html
resource "aws_kms_ciphertext" "slack_url" {
  plaintext = "https://hooks.slack.com/services/AAA/BBB/CCC"
  key_id    = aws_kms_key.this.arn
}

module "notify_slack" {
  source = "../../"

  sns_topic_name = "slack-topic"

  slack_webhook_url = aws_kms_ciphertext.slack_url.ciphertext_blob
  slack_channel     = "aws-notification"
  slack_username    = "reporter"

  kms_key_arn = aws_kms_key.this.arn

  lambda_description = "Lambda function which sends notifications to Slack"
  log_events         = true

  tags = {
    Name = "cloudwatch-alerts-to-slack"
  }
}

resource "aws_cloudwatch_metric_alarm" "LambdaDuration" {
  alarm_name          = "NotifySlackDuration"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Average"
  threshold           = "5000"
  alarm_description   = "Duration of notifying slack exceeds threshold"

  alarm_actions = [module.notify_slack.this_slack_topic_arn]

  dimensions = {
    FunctionName = module.notify_slack.notify_slack_lambda_function_name
  }
}
