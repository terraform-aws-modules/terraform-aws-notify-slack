data "aws_sns_topic" "this" {
  count = false == var.create_sns_topic && var.create ? 1 : 0

  name = var.sns_topic_name
}

resource "aws_sns_topic" "this" {
  count = var.create_sns_topic && var.create ? 1 : 0

  name = var.sns_topic_name

  tags = merge(var.tags, var.sns_topic_tags)
}

locals {
  sns_topic_arn = element(
    concat(
      aws_sns_topic.this.*.arn,
      data.aws_sns_topic.this.*.arn,
      [""],
    ),
    0,
  )
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = var.lambda_log_retention
}

resource "aws_sns_topic_subscription" "sns_notify_slack" {
  count = var.create ? 1 : 0

  topic_arn = local.sns_topic_arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.notify_slack[0].arn
}

resource "aws_lambda_permission" "sns_notify_slack" {
  count = var.create ? 1 : 0

  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.notify_slack[0].function_name
  principal     = "sns.amazonaws.com"
  source_arn    = local.sns_topic_arn
}

data "null_data_source" "lambda_file" {
  inputs = {
    filename = "${path.module}/functions/notify_slack.py"
  }
}

data "null_data_source" "lambda_archive" {
  inputs = {
    filename = "${path.module}/functions/notify_slack.zip"
  }
}

data "archive_file" "notify_slack" {
  count = var.create ? 1 : 0

  type        = "zip"
  source_file = data.null_data_source.lambda_file.outputs.filename
  output_path = data.null_data_source.lambda_archive.outputs.filename
}

resource "aws_lambda_function" "notify_slack" {
  count = var.create ? 1 : 0

  filename = data.archive_file.notify_slack[0].output_path

  function_name = var.lambda_function_name

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
    }
  }

  lifecycle {
    ignore_changes = [
      filename,
      last_modified,
    ]
  }

  tags = merge(var.tags, var.lambda_function_tags)

  depends_on = ["aws_cloudwatch_log_group.lambda"]
}
