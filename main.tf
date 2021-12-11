data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_region" "current" {}

locals {
  sns_topic_arn = try(
    aws_sns_topic.this[0].arn,
    "arn:${data.aws_partition.current.id}:sns:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${var.sns_topic_name}",
    ""
  )

  aws_lambda_powertools_layer = substr(data.aws_region.current.name, 0, 6) != "us-gov-" ? "arn:aws:lambda:${data.aws_region.current.name}:017000801446:layer:AWSLambdaPowertoolsPython:4" : ""

  lambda_layers = compact(distinct(concat(var.lambda_layers, [local.aws_lambda_powertools_layer])))
}

################################################################################
# SNS Topic
################################################################################

resource "aws_sns_topic" "this" {
  count = var.create_sns_topic && var.create ? 1 : 0

  name              = var.sns_topic_name
  kms_master_key_id = var.sns_topic_kms_key_id

  tags = merge(var.tags, var.sns_topic_tags)
}


resource "aws_sns_topic_subscription" "sns_notify_slack" {
  count = var.create ? 1 : 0

  topic_arn     = local.sns_topic_arn
  protocol      = "lambda"
  endpoint      = module.lambda.lambda_function_arn
  filter_policy = var.subscription_filter_policy
}

################################################################################
# Lambda Function
################################################################################

data "archive_file" "lambda" {
  count = var.create ? 1 : 0

  type             = "zip"
  source_dir       = "${path.module}/functions"
  output_file_mode = "0666"
  output_path      = "${path.module}/notify_zip.zip"
  excludes         = [".mypy_cache", ".pytest_cache", "tests", ".coverage", ".flake8", ".int.env", "Pipfile", "Pipfile.lock", "pyproject.toml", "README.md"]
}

module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "2.27.1"

  create = var.create

  function_name = var.lambda_function_name
  description   = var.lambda_description

  handler                  = "notify_slack.lambda_handler"
  create_package           = false
  local_existing_package   = data.archive_file.lambda[0].output_path
  recreate_missing_package = var.recreate_missing_package

  runtime = var.lambda_runtime
  timeout = var.lambda_timeout
  layers  = local.lambda_layers

  kms_key_arn                    = var.kms_key_arn
  reserved_concurrent_executions = var.reserved_concurrent_executions

  # If publish is disabled, there will be "Error adding new Lambda Permission for notify_slack:
  # InvalidParameterValueException: We currently do not support adding policies for $LATEST."
  publish = true

  environment_variables = {
    SLACK_WEBHOOK_URL = var.slack_webhook_url
    SLACK_CHANNEL     = var.slack_channel
    SLACK_USERNAME    = var.slack_username
    SLACK_EMOJI       = var.slack_emoji
    LOG_EVENTS        = var.log_events ? "True" : "False"
  }

  create_role               = var.lambda_role == ""
  lambda_role               = var.lambda_role
  role_name                 = "${var.iam_role_name_prefix}-${var.lambda_function_name}"
  role_permissions_boundary = var.iam_role_boundary_policy_arn
  role_tags                 = var.iam_role_tags
  role_path                 = var.iam_role_path
  policy_path               = var.iam_policy_path

  attach_network_policy = var.lambda_function_vpc_subnet_ids != null

  allowed_triggers = {
    AllowExecutionFromSNS = {
      principal  = "sns.amazonaws.com"
      source_arn = local.sns_topic_arn
    }
  }

  store_on_s3 = var.lambda_function_store_on_s3
  s3_bucket   = var.lambda_function_s3_bucket

  vpc_subnet_ids         = var.lambda_function_vpc_subnet_ids
  vpc_security_group_ids = var.lambda_function_vpc_security_group_ids

  # CloudWatch log group
  cloudwatch_logs_retention_in_days = var.cloudwatch_log_group_retention_in_days
  cloudwatch_logs_kms_key_id        = var.cloudwatch_log_group_kms_key_id
  cloudwatch_logs_tags              = var.cloudwatch_log_group_tags

  tags = merge(var.tags, var.lambda_function_tags)
}
