provider "aws" {
  region = "eu-west-1"
}

module "notify_slack" {
  source = "../../"

  sns_topic_name = "slack-topic"

  slack_webhook_url = "https://hooks.slack.com/services/AAA/BBB/CCC"
  slack_channel     = "aws-notification"
  slack_username    = "reporter"
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

  alarm_actions = ["${module.notify_slack.this_slack_topic_arn}"]

  dimensions {
    FunctionName = "${module.notify_slack.notify_slack_lambda_function_name}"
  }
}
