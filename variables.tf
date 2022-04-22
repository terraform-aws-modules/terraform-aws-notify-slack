variable "create" {
  description = "Whether to create all resources"
  type        = bool
  default     = true
}

variable "create_sns_topic" {
  description = "Whether to create new SNS topic"
  type        = bool
  default     = true
}

variable "lambda_function_name" {
  description = "The name of the Lambda function to create"
  type        = string
  default     = "notify_slack"
}

variable "sns_topic_name" {
  description = "The name of the SNS topic to create"
  type        = string
}

variable "slack_webhook_url" {
  description = "The URL of Slack webhook"
  type        = string
}

variable "slack_channel" {
  description = "The name of the channel in Slack for notifications"
  type        = string
}

variable "slack_username" {
  description = "The username that will appear on Slack messages"
  type        = string
}

variable "slack_emoji" {
  description = "A custom emoji that will appear on Slack messages"
  type        = string
  default     = ":aws:"
}

variable "kms_key_arn" {
  description = "ARN of the KMS key used for decrypting slack webhook url"
  type        = string
  default     = ""
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}

variable "iam_role_tags" {
  description = "Additional tags for the IAM role"
  type        = map(string)
  default     = {}
}

variable "lambda_function_tags" {
  description = "Additional tags for the Lambda function"
  type        = map(string)
  default     = {}
}

variable "sns_topic_tags" {
  description = "Additional tags for the SNS topic"
  type        = map(string)
  default     = {}
}

variable "python_version" {
  description = "The Runtime Python version"
  type        = string
  default     = "python3.9"
}
