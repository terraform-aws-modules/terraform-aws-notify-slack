variable "slack_topic_name" {
  description = "The name of the SNS topic for slack"
}

variable "slack_webhook_url" {
  description = "The URL of Slack webhook"
}

variable "slack_channel" {
  description = "The name of the channel in Slack for notifications"
}

variable "kms_key_arn" {
  description = "ARN of the KMS key used for decrypting slack webhook url"
}
