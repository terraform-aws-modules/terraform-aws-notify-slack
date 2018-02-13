variable "create_sns_topic" {
  description = "Whether to create new SNS topic"
  default     = true
}

variable "sns_topic_name" {
  description = "The name of the SNS topic to create"
}

variable "slack_webhook_url" {
  description = "The URL of Slack webhook"
}

variable "slack_channel" {
  description = "The name of the channel in Slack for notifications"
}

variable "kms_key_arn" {
  description = "ARN of the KMS key used for decrypting slack webhook url"
  default     = ""
}
