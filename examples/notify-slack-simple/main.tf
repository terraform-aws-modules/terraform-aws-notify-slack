module "notify_slack" {
  source = "../../"

  slack_topic_name = "slack-topic"

  slack_webhook_url = "https://hooks.slack.com/services/AAA/BBB/CCC"

  slack_channel = "aws-notification"
}
