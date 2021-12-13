provider "aws" {
  region = "eu-west-1"
}


module "notify_slack" {
  source = "../../"

  for_each = toset([
    "develop",
    "release",
    "test",
  ])

  sns_topic_name = "slack-topic"

  lambda_function_name = "notify_slack_${each.value}"

  # Note: this needs to exist in your account already in SSM
  # and should be set as a SecureString
  slack_webhook_url_ssm_parameter_name = "/example/notify_slack/webhook_url"
  environment_variables = {
    SLACK_USERNAME = "reporter"
    SLACK_EMOJI    = ":wave:"
    LOG_EVENTS     = "True"
  }

  lambda_description = "Lambda function which sends notifications to Slack"

  # VPC
  #  lambda_function_vpc_subnet_ids = module.vpc.intra_subnets
  #  lambda_function_vpc_security_group_ids = [module.vpc.default_security_group_id]

  tags = {
    Name = "cloudwatch-alerts-to-slack"
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_duration" {
  alarm_name          = "NotifySlackDuration"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Average"
  threshold           = "5000"
  alarm_description   = "Duration of notifying slack exceeds threshold"

  alarm_actions = [module.notify_slack["develop"].slack_topic_arn]

  dimensions = {
    FunctionName = module.notify_slack["develop"].notify_slack_lambda_function_name
  }
}

######
# VPC
######
resource "random_pet" "this" {
  length = 2
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = random_pet.this.id
  cidr = "10.10.0.0/16"

  azs           = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  intra_subnets = ["10.10.101.0/24", "10.10.102.0/24", "10.10.103.0/24"]
}
