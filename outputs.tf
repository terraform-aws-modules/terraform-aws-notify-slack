output "this_slack_topic_name" {
  description = "The name of the created SNS topic for Slack"
  value       = "${aws_sns_topic.slack_topic.name}"
}

output "this_slack_topic_arn" {
  description = "ARN of the created SNS topic for Slack"
  value       = "${aws_sns_topic.slack_topic.arn}"
}
