output "this_sns_topic_arn" {
  description = "The ARN of the created SNS topic from which messages will be sent to Slack"
  value       = "${module.notify_slack.this_slack_topic_arn}"
}
