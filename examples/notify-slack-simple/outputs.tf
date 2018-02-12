output "sns_topic_arn" {
  description = "ARN of the created SNS topic for Slack"
  value       = "${module.notify_slack.this_slack_topic_arn}"
}
