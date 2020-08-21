provider "aws" {
  region = "eu-west-1"
}

resource "aws_sns_topic" "my_sns" {
  name = "my-sns"
}

module "notify_slack" {
  source = "../../"

  sns_topic_name   = aws_sns_topic.my_sns.name
  create_sns_topic = false

  slack_webhook_url = "https://hooks.slack.com/services/AAA/BBB/CCC"
  slack_channel     = "aws-notification"
  slack_username    = "reporter"

  tags = {
    Name = "notify-slack-simple"
  }

  depends_on = [aws_sns_topic.my_sns]
}
