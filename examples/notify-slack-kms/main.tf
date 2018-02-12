resource "aws_kms_key" "lambda_kms_key" {
  description             = "KMS key 1"
  deletion_window_in_days = 10
}

# Encrypt the URL, this is an example, in practice encryption should not be done here as it will be shown in logs.
data "aws_kms_ciphertext" "slack_url" {
  key_id    = "${aws_kms_key.lambda_kms_key.key_id}"
  plaintext = "https://hooks.slack.com/services/AAA/BBB/CCC"
}

module "notify_slack" {
  source = "../../"

  slack_topic_name = "slack-topic"

  slack_webhook_url = "${data.aws_kms_ciphertext.slack_url.ciphertext_blob}"

  slack_channel = "aws-notification"

  kms_key_arn = "${aws_kms_key.lambda_kms_key.arn}"
}
