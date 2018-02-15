provider "aws" {
  region = "eu-west-1"
}

variable "kms_key_arn" {
  default = "arn:aws:kms:eu-west-1:835367859851:key/054b4846-95fe-4537-94f2-1dfd255238cf"
}

# Encrypt the URL, this is an example, in practice encryption should not be done here as it will be shown in logs and end up in Terraform state file
data "aws_kms_ciphertext" "slack_url" {
  plaintext = "https://hooks.slack.com/services/AAA/BBB/CCC"
  key_id    = "${var.kms_key_arn}"
}

module "notify_slack" {
  source = "../../"

  sns_topic_name = "slack-topic"

  slack_webhook_url = "${data.aws_kms_ciphertext.slack_url.ciphertext_blob}"
  slack_channel     = "aws-notification"
  slack_username    = "reporter"

  # Option 1
//   kms_key_arn = "${aws_kms_key.this.arn}"

  # Option 2
//  kms_key_arn = "${data.aws_kms_alias.this.target_key_arn}"

  # Option 3
  kms_key_arn = "${var.kms_key_arn}"
}
