data "archive_file" "lambda_function" {
  type        = "zip"
  source_file = "${path.module}/functions/notify_slack.py"
  output_path = "${path.module}/files/notify_slack_lambda.zip"
}

resource "aws_sns_topic" "slack_topic" {
  name = "${var.slack_topic_name}"
}

resource "aws_sns_topic_subscription" "lambda-subscription" {
  topic_arn = "${aws_sns_topic.slack_topic.arn}"
  protocol  = "lambda"
  endpoint  = "${aws_lambda_function.notify_slack_lambda.arn}"
}

resource "aws_lambda_function" "notify_slack_lambda" {
  filename         = "${path.module}/files/notify_slack_lambda.zip"
  function_name    = "notify_slack"
  role             = "${aws_iam_role.iam_for_lambda.arn}"
  handler          = "notify_slack.lambda_handler"
  source_code_hash = "${data.archive_file.lambda_function.output_base64sha256}"
  runtime          = "python3.6"
  timeout          = "30"
  kms_key_arn      = "${var.kms_key_arn}"

  environment {
    variables = {
      SLACK_WEBHOOK = "${var.slack_webhook_url}"
      SLACK_CHANNEL = "${var.slack_channel}"
    }
  }
}

resource "aws_lambda_permission" "sns_lambda_permission" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.notify_slack_lambda.function_name}"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.slack_topic.arn}"
}
