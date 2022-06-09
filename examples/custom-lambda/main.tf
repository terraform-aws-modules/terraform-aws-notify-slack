module "notify_slack" {
  source = "../../"

  lambda_function_name = "custom-lambda"
  lambda_source_path   = "mylambda.py"

  sns_topic_name = "custom-lambda"

  slack_webhook_url = "https://hooks.slack.com/services/AAA/BBB/CCC"
  slack_channel     = "aws-notification"
  slack_username    = "reporter"
}
