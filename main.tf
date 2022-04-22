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
  lambda_filename = "${path.module}/functions/notify_slack.py"
  lambda_archive  = "${path.module}/functions/notify_slack.zip"
  sns_topic_arn = element(
    concat(
      aws_sns_topic.this.*.arn,
      data.aws_sns_topic.this.*.arn,
      [""],
    ),
    0,
  )
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

data "archive_file" "notify_slack" {
  count = var.create ? 1 : 0

  type        = "zip"
  source_file = local.lambda_filename
  output_path = local.lambda_archive
}

resource "aws_lambda_function" "notify_slack" {
  count = var.create ? 1 : 0

  filename = data.archive_file.notify_slack[0].output_path

  function_name = var.lambda_function_name

  role             = aws_iam_role.lambda[0].arn
  handler          = "notify_slack.lambda_handler"
  source_code_hash = data.archive_file.notify_slack[0].output_base64sha256
  runtime          = var.python_version
  timeout          = 30
  kms_key_arn      = var.kms_key_arn

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
      # filename, # removing this as its no longer needed since the file name is realitive
      last_modified,
    ]
  }

  tags = merge(var.tags, var.lambda_function_tags)

  tracing_config {
    mode = "Active"
  }
}

