provider "aws" {
  region = "eu-west-1"
}

variable "kms_key_arn" {
  default = "arn:aws:kms:eu-west-1:000014191260:key/66db1c5d-d42b-4e28-8efb-07a9cf607a73"
}

# Encrypt the URL, this is an example, in practice encryption should not be done here as it will be shown in logs and end up in Terraform state file
data "aws_kms_ciphertext" "slack_url" {
  plaintext = "https://hooks.slack.com/services/AAA/BBB/CCC"
  key_id    = "${var.kms_key_arn}"
}

module "notify_slack" {
  source = "../../"

  sns_topic_name = "slack-topic"

  slack_webhook_url = "${data.aws_kms_ciphertext.slack_url.ciphertext_blob}"
  slack_channel     = "aws-notification"
  slack_username    = "reporter"

  # Option 1
  //   kms_key_arn = "${aws_kms_key.this.arn}"


  # Option 2
  //  kms_key_arn = "${data.aws_kms_alias.this.target_key_arn}"

  # Option 3
  kms_key_arn = "${var.kms_key_arn}"
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
