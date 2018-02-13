provider "aws" {
  region = "eu-west-1"
}

resource "aws_kms_key" "this" {
  description = "KMS key for notify-slack test"
}

# Encrypt the URL, this is an example, in practice encryption should not be done here as it will be shown in logs and end up in Terraform state file
data "aws_kms_ciphertext" "slack_url" {
  plaintext = "https://hooks.slack.com/services/AAA/BBB/CCC"
  key_id    = "${aws_kms_key.this.key_id}"
}

module "notify_slack" {
  source = "../../"

  sns_topic_name = "slack-topic"

  slack_webhook_url = "${data.aws_kms_ciphertext.slack_url.ciphertext_blob}"

  slack_channel = "aws-notification"

  kms_key_arn = "${aws_kms_key.this.arn}"
}
