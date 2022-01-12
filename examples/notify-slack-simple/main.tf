provider "aws" {
  region = local.region
}

locals {
  name   = "ex-${replace(basename(path.cwd), "_", "-")}"
  region = "eu-west-1"
  tags = {
    Owner       = "user"
    Environment = "dev"
  }
}

################################################################################
# Supporting Resources
################################################################################

resource "aws_sns_topic" "example" {
  name = local.name
  tags = local.tags
}

################################################################################
# Slack Notify Module
################################################################################

module "notify_slack" {
  source = "../../"

  sns_topic_name   = aws_sns_topic.example.name
  create_sns_topic = false

  # Note: this needs to exist in your account already in SSM
  # and should be set as a SecureString
  slack_webhook_url_ssm_parameter_name = "/example/notify_slack/webhook_url"
  environment_variables = {
    SLACK_USERNAME = "reporter"
    SLACK_EMOJI    = ":wave:"
    LOG_EVENTS     = "True"
  }

  tags = local.tags
}

################################################################################
# Integration Testing Support
# This populates a file that is gitignored to aid in executing the integration tests locally
################################################################################

resource "local_file" "integration_testing" {
  filename = "${path.module}/../../functions/.int.env"
  content  = <<-EOT
    REGION=${local.region}
    LAMBDA_FUNCTION_NAME=${module.notify_slack.notify_slack_lambda_function_name}
    SNS_TOPIC_ARN=${aws_sns_topic.example.arn}
    EOT
}
