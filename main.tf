data "aws_sns_topic" "this" {
  count = "${(1 - var.create_sns_topic) * var.enable}"

  name = "${var.sns_topic_name}"
}

resource "aws_sns_topic" "this" {
  count = "${var.create_sns_topic * var.enable}"

  name = "${var.sns_topic_name}"
}

locals {
  sns_topic_arn      = "${element(compact(concat(aws_sns_topic.this.*.arn, data.aws_sns_topic.this.*.arn, list(var.enable))), 0)}"
  function_name_base = "${format("%s-%s", var.lambda_function_name, var.sns_topic_name)}"
}

resource "aws_sns_topic_subscription" "sns_notify_slack" {
  count = "${var.enable}"

  topic_arn = "${local.sns_topic_arn}"
  protocol  = "lambda"
  endpoint  = "${aws_lambda_function.notify_slack.0.arn}"
}

resource "aws_lambda_permission" "sns_notify_slack" {
  count = "${var.enable}"

  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.notify_slack.0.function_name}"
  principal     = "sns.amazonaws.com"
  source_arn    = "${local.sns_topic_arn}"
}

data "archive_file" "notify_slack" {
  count = "${var.enable}"

  type        = "zip"
  source_file = "${path.module}/functions/notify_slack.py"
  output_path = "${path.module}/functions/notify_slack.zip"
}

resource "aws_lambda_function" "notify_slack" {
  count = "${var.enable}"

  filename = "${data.archive_file.notify_slack.0.output_path}"

  function_name = "${substr(local.function_name_base, 0, length(local.function_name_base) > 64 ? 64 : length(local.function_name_base))}"

  role             = "${aws_iam_role.lambda.arn}"
  handler          = "notify_slack.lambda_handler"
  source_code_hash = "${data.archive_file.notify_slack.0.output_base64sha256}"
  runtime          = "python3.6"
  timeout          = 30
  kms_key_arn      = "${var.kms_key_arn}"

  environment {
    variables = {
      SLACK_WEBHOOK_URL = "${var.slack_webhook_url}"
      SLACK_CHANNEL     = "${var.slack_channel}"
      SLACK_USERNAME    = "${var.slack_username}"
      SLACK_EMOJI       = "${var.slack_emoji}"
    }
  }

  lifecycle {
    ignore_changes = [
      "filename",
      "last_modified",
    ]
  }
}
