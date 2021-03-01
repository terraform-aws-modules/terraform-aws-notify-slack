data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_sns_topic" "this" {
  count = var.create_sns_topic && var.create ? 1 : 0

  name = var.sns_topic_name

  kms_master_key_id = var.sns_topic_kms_key_id

  tags = merge(var.tags, var.sns_topic_tags)
}

locals {
  sns_topic_arn = element(
    concat(
      aws_sns_topic.this.*.arn,
      ["arn:aws:sns:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${var.sns_topic_name}"],
      [""]
    ),
    0,
  )

  lambda_policy_document = {
    sid       = "AllowWriteToCloudwatchLogs"
    effect    = "Allow"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = [replace("${element(concat(aws_cloudwatch_log_group.lambda[*].arn, list("")), 0)}:*", ":*:*", ":*")]
  }

  lambda_policy_document_kms = {
    sid       = "AllowKMSDecrypt"
    effect    = "Allow"
    actions   = ["kms:Decrypt"]
    resources = [var.kms_key_arn]
  }
}

data "aws_iam_policy_document" "lambda" {
  count = var.create ? 1 : 0

  dynamic "statement" {
    for_each = concat([local.lambda_policy_document], var.kms_key_arn != "" ? [local.lambda_policy_document_kms] : [])
    content {
      sid       = statement.value.sid
      effect    = statement.value.effect
      actions   = statement.value.actions
      resources = statement.value.resources
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda" {
  count = var.create ? 1 : 0

  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = var.cloudwatch_log_group_retention_in_days
  kms_key_id        = var.cloudwatch_log_group_kms_key_id

  tags = merge(var.tags, var.cloudwatch_log_group_tags)
}

resource "aws_sns_topic_subscription" "sns_notify_slack" {
  count = var.create ? 1 : 0

  topic_arn     = local.sns_topic_arn
  protocol      = "lambda"
  endpoint      = module.lambda.this_lambda_function_arn
  filter_policy = var.subscription_filter_policy
}

module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "1.28.0"

  create = var.create

  function_name = var.lambda_function_name
  description   = var.lambda_description

  handler                        = "notify_slack.lambda_handler"
  source_path                    = "${path.module}/functions/notify_slack.py"
  runtime                        = "python3.8"
  timeout                        = 30
  kms_key_arn                    = var.kms_key_arn
  reserved_concurrent_executions = var.reserved_concurrent_executions

  # If publish is disabled, there will be "Error adding new Lambda Permission for notify_slack: InvalidParameterValueException: We currently do not support adding policies for $LATEST."
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

  # Do not use Lambda's policy for cloudwatch logs, because we have to add a policy
  # for KMS conditionally. This way attach_policy_json is always true independenty of
  # the value of presense of KMS. Famous "computed values in count" bug...
  attach_cloudwatch_logs_policy = false
  attach_policy_json            = true
  policy_json                   = element(concat(data.aws_iam_policy_document.lambda[*].json, [""]), 0)

  use_existing_cloudwatch_log_group = true
  attach_network_policy             = var.lambda_function_vpc_subnet_ids != null

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

  tags = merge(var.tags, var.lambda_function_tags)

  depends_on = [aws_cloudwatch_log_group.lambda]
}
