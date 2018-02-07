output "this_slack_topic_name" {
  description = "The name of the slack topic"
  value       = "${aws_sns_topic.slack_topic.name}"
}
