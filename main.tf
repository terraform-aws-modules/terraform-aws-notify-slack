data "aws_sns_topic" "notify" {
  count = false == var.create_notify_sns_topic && var.create ? 1 : 0

  name = var.notify_sns_topic_name
}

data "aws_sns_topic" "approve" {
  count = false == var.create_approve_sns_topic && var.create ? 1 : 0

  name = var.approve_sns_topic_name
}

resource "aws_sns_topic" "notify" {
  count = var.create_notify_sns_topic && var.create ? 1 : 0

  name = var.notify_sns_topic_name

  tags = merge(var.tags, var.sns_topic_tags)
}

resource "aws_sns_topic" "approve" {
  count = var.create_approve_sns_topic && var.create ? 1 : 0

  name = var.approve_sns_topic_name

  tags = merge(var.tags, var.sns_topic_tags)
}

locals {
  notify_sns_topic_arn = element(
    concat(
      aws_sns_topic.notify.*.arn,
      data.aws_sns_topic.notify.*.arn,
      [""],
    ),
    0,
  )
  approve_sns_topic_arn = element(
    concat(
      aws_sns_topic.approve.*.arn,
      data.aws_sns_topic.approve.*.arn,
      [""],
    ),
    0,
  )
}

resource "aws_cloudwatch_log_group" "notify_lambda" {
  count = var.create ? 1 : 0

  name              = "/aws/lambda/${var.notify_lambda_function_name}"
  retention_in_days = var.cloudwatch_log_group_retention_in_days
  kms_key_id        = var.cloudwatch_log_group_kms_key_id

  tags = merge(var.tags, var.cloudwatch_log_group_tags)
}

resource "aws_cloudwatch_log_group" "approve_request_lambda" {
  count = var.create ? 1 : 0

  name              = "/aws/lambda/${var.approve_request_lambda_function_name}"
  retention_in_days = var.cloudwatch_log_group_retention_in_days
  kms_key_id        = var.cloudwatch_log_group_kms_key_id

  tags = merge(var.tags, var.cloudwatch_log_group_tags)
}

resource "aws_cloudwatch_log_group" "approve_response_lambda" {
  count = var.create ? 1 : 0

  name              = "/aws/lambda/${var.approve_response_lambda_function_name}"
  retention_in_days = var.cloudwatch_log_group_retention_in_days
  kms_key_id        = var.cloudwatch_log_group_kms_key_id

  tags = merge(var.tags, var.cloudwatch_log_group_tags)
}

resource "aws_sns_topic_subscription" "sns_notify_slack" {
  count = var.create ? 1 : 0

  topic_arn = local.notify_sns_topic_arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.notify_slack[0].arn
}

resource "aws_sns_topic_subscription" "sns_approve_request_slack" {
  count = var.create ? 1 : 0

  topic_arn = local.approve_sns_topic_arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.approve_request_slack[0].arn
}

resource "aws_sns_topic_subscription" "sns_approve_response_slack" {
  count = var.create ? 1 : 0

  topic_arn = local.approve_sns_topic_arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.approve_response_slack[0].arn
}

resource "aws_lambda_permission" "sns_notify_slack" {
  count = var.create ? 1 : 0

  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.notify_slack[0].function_name
  principal     = "sns.amazonaws.com"
  source_arn    = local.notify_sns_topic_arn
}

resource "aws_lambda_permission" "sns_approve_request_slack" {
  count = var.create ? 1 : 0

  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.approve_request_slack[0].function_name
  principal     = "sns.amazonaws.com"
  source_arn    = local.approve_sns_topic_arn
}

resource "aws_lambda_permission" "sns_approve_response_slack" {
  count = var.create ? 1 : 0

  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.approve_response_slack[0].function_name
  principal     = "sns.amazonaws.com"
  source_arn    = local.approve_sns_topic_arn
}

data "null_data_source" "notify_lambda_file" {
  inputs = {
    filename = "${path.module}/functions/notify_slack.py"
  }
}

data "null_data_source" "approve_request_lambda_file" {
  inputs = {
    filename = "${path.module}/functions/approve_request_slack.py"
  }
}

data "null_data_source" "approve_response_lambda_file" {
  inputs = {
    filename = "${path.module}/functions/approve_response_slack.py"
  }
}

data "null_data_source" "notify_lambda_archive" {
  inputs = {
    filename = "${path.module}/functions/notify_slack.zip"
  }
}

data "null_data_source" "approve_request_lambda_archive" {
  inputs = {
    filename = "${path.module}/functions/approve_request_slack.zip"
  }
}

data "null_data_source" "approve_response_lambda_archive" {
  inputs = {
    filename = "${path.module}/functions/approve_response_slack.zip"
  }
}

data "archive_file" "notify_slack" {
  count = var.create ? 1 : 0

  type        = "zip"
  source_file = data.null_data_source.notify_lambda_file.outputs.filename
  output_path = data.null_data_source.notify_lambda_archive.outputs.filename
}

data "archive_file" "approve_request_slack" {
  count = var.create ? 1 : 0

  type        = "zip"
  source_file = data.null_data_source.approve_request_lambda_file.outputs.filename
  output_path = data.null_data_source.approve_request_lambda_archive.outputs.filename
}

data "archive_file" "approve_response_slack" {
  count = var.create ? 1 : 0

  type        = "zip"
  source_file = data.null_data_source.approve_response_lambda_file.outputs.filename
  output_path = data.null_data_source.approve_response_lambda_archive.outputs.filename
}

resource "aws_lambda_function" "notify_slack" {
  count = var.create ? 1 : 0

  filename = data.archive_file.notify_slack[0].output_path

  function_name = var.approve_response_lambda_function_name
  description   = var.approve_response_lambda_description

  role                           = aws_iam_role.lambda[0].arn
  handler                        = "notify_slack.lambda_handler"
  source_code_hash               = data.archive_file.notify_slack[0].output_base64sha256
  runtime                        = "python3.7"
  timeout                        = 30
  kms_key_arn                    = var.kms_key_arn
  reserved_concurrent_executions = var.reserved_concurrent_executions

  environment {
    variables = {
      SLACK_WEBHOOK_URL = var.slack_webhook_url
      SLACK_CHANNEL     = var.slack_channel
      SLACK_USERNAME    = var.slack_username
      SLACK_EMOJI       = var.slack_emoji
      LOG_EVENTS        = var.log_events ? "True" : "False"
    }
  }

  tags = merge(var.tags, var.lambda_function_tags)

  lifecycle {
    ignore_changes = [
      filename,
      last_modified,
    ]
  }

  depends_on = [aws_cloudwatch_log_group.notify_lambda]
}

resource "aws_lambda_function" "approve_request_slack" {
  count = var.create ? 1 : 0

  filename = data.archive_file.approve_request_slack[0].output_path

  function_name = var.approve_request_lambda_function_name
  description   = var.approve_request_lambda_description

  role                           = aws_iam_role.lambda[0].arn
  handler                        = "approve_request_slack.lambda_handler"
  source_code_hash               = data.archive_file.approve_request_slack[0].output_base64sha256
  runtime                        = "python3.7"
  timeout                        = 30
  kms_key_arn                    = var.kms_key_arn
  reserved_concurrent_executions = var.reserved_concurrent_executions

  environment {
    variables = {
      SLACK_WEBHOOK_URL        = var.slack_webhook_url
      SLACK_CHANNEL            = var.slack_channel
      SLACK_USERNAME           = var.slack_username
      SLACK_VERIFICATION_TOKEN = var.slack_verification_token
      SLACK_EMOJI              = var.slack_emoji
      LOG_EVENTS               = var.log_events ? "True" : "False"
    }
  }

  tags = merge(var.tags, var.lambda_function_tags)

  lifecycle {
    ignore_changes = [
      filename,
      last_modified,
    ]
  }

  depends_on = [aws_cloudwatch_log_group.approve_request_lambda]
}

resource "aws_lambda_function" "approve_response_slack" {
  count = var.create ? 1 : 0

  filename = data.archive_file.approve_response_slack[0].output_path

  function_name = var.approve_response_lambda_function_name
  description   = var.approve_response_lambda_description

  role                           = aws_iam_role.lambda[0].arn
  handler                        = "approve_response_slack.lambda_handler"
  source_code_hash               = data.archive_file.approve_response_slack[0].output_base64sha256
  runtime                        = "python3.7"
  timeout                        = 30
  kms_key_arn                    = var.kms_key_arn
  reserved_concurrent_executions = var.reserved_concurrent_executions

  environment {
    variables = {
      SLACK_WEBHOOK_URL        = var.slack_webhook_url
      SLACK_CHANNEL            = var.slack_channel
      SLACK_USERNAME           = var.slack_username
      SLACK_VERIFICATION_TOKEN = var.slack_verification_token
      SLACK_EMOJI              = var.slack_emoji
      LOG_EVENTS               = var.log_events ? "True" : "False"
    }
  }

  tags = merge(var.tags, var.lambda_function_tags)

  lifecycle {
    ignore_changes = [
      filename,
      last_modified,
    ]
  }

  depends_on = [aws_cloudwatch_log_group.approve_response_lambda]
}
