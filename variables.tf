variable "putin_khuylo" {
  description = "Do you agree that Putin doesn't respect Ukrainian sovereignty and territorial integrity? More info: https://en.wikipedia.org/wiki/Putin_khuylo!"
  type        = bool
  default     = true
}

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

variable "hash_extra" {
  description = "The string to add into hashing function. Useful when building same source path for different functions."
  type        = string
  default     = ""
}

variable "lambda_function_code_signing_config_arn" {
  description = "Amazon Resource Name (ARN) of the Lambda Code Signing Configuration"
  type        = string
  default     = null
}

variable "lambda_role" {
  description = "IAM role attached to the Lambda Function.  If this is set then a role will not be created for you."
  type        = string
  default     = ""
}

variable "lambda_function_name" {
  description = "The name of the Lambda function to create"
  type        = string
  default     = "notify_slack"
}

variable "lambda_description" {
  description = "The description of the Lambda function"
  type        = string
  default     = null
}

variable "lambda_source_path" {
  description = "The source path of the custom Lambda function"
  type        = string
  default     = null
}

variable "lambda_dead_letter_target_arn" {
  description = "The ARN of an SNS topic or SQS queue to notify when an invocation fails."
  type        = string
  default     = null
}

variable "lambda_attach_dead_letter_policy" {
  description = "Controls whether SNS/SQS dead letter notification policy should be added to IAM role for Lambda Function"
  type        = bool
  default     = false
}

variable "sns_topic_name" {
  description = "The name of the SNS topic to create"
  type        = string
}

variable "sns_topic_kms_key_id" {
  description = "ARN of the KMS key used for enabling SSE on the topic"
  type        = string
  default     = ""
}

variable "enable_sns_topic_delivery_status_logs" {
  description = "Whether to enable SNS topic delivery status logs"
  type        = bool
  default     = false
}

variable "sns_topic_lambda_feedback_role_arn" {
  description = "IAM role for SNS topic delivery status logs.  If this is set then a role will not be created for you."
  type        = string
  default     = ""
}

variable "sns_topic_feedback_role_name" {
  description = "Name of the IAM role to use for SNS topic delivery status logging"
  type        = string
  default     = null
}

variable "sns_topic_feedback_role_description" {
  description = "Description of IAM role to use for SNS topic delivery status logging"
  type        = string
  default     = null
}

variable "sns_topic_feedback_role_path" {
  description = "Path of IAM role to use for SNS topic delivery status logging"
  type        = string
  default     = null
}

variable "sns_topic_feedback_role_force_detach_policies" {
  description = "Specifies to force detaching any policies the IAM role has before destroying it."
  type        = bool
  default     = true
}

variable "sns_topic_feedback_role_permissions_boundary" {
  description = "The ARN of the policy that is used to set the permissions boundary for the IAM role used by SNS topic delivery status logging"
  type        = string
  default     = null
}

variable "sns_topic_feedback_role_tags" {
  description = "A map of tags to assign to IAM the SNS topic feedback role"
  type        = map(string)
  default     = {}
}

variable "sns_topic_lambda_feedback_sample_rate" {
  description = "The percentage of successful deliveries to log"
  type        = number
  default     = 100
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

variable "s3_existing_package" {
  description = "The path to the existing Lambda package in S3"
  type        = map(string)
  default     = null
}

variable "kms_key_arn" {
  description = "ARN of the KMS key used for decrypting slack webhook url"
  type        = string
  default     = ""
}

variable "recreate_missing_package" {
  description = "Whether to recreate missing Lambda package if it is missing locally or not"
  type        = bool
  default     = true
}

variable "log_events" {
  description = "Boolean flag to enabled/disable logging of incoming events"
  type        = bool
  default     = false
}

variable "reserved_concurrent_executions" {
  description = "The amount of reserved concurrent executions for this lambda function. A value of 0 disables lambda from being triggered and -1 removes any concurrency limitations"
  type        = number
  default     = -1
}

variable "cloudwatch_log_group_retention_in_days" {
  description = "Specifies the number of days you want to retain log events in log group for Lambda."
  type        = number
  default     = 0
}

variable "cloudwatch_log_group_kms_key_id" {
  description = "The ARN of the KMS Key to use when encrypting log data for Lambda"
  type        = string
  default     = null
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

variable "iam_role_boundary_policy_arn" {
  description = "The ARN of the policy that is used to set the permissions boundary for the role"
  type        = string
  default     = null
}

variable "iam_role_name_prefix" {
  description = "A unique role name beginning with the specified prefix"
  type        = string
  default     = "lambda"
}

variable "iam_role_path" {
  description = "Path of IAM role to use for Lambda Function"
  type        = string
  default     = null
}

variable "iam_policy_path" {
  description = "Path of policies to that should be added to IAM role for Lambda Function"
  type        = string
  default     = null
}

variable "lambda_function_tags" {
  description = "Additional tags for the Lambda function"
  type        = map(string)
  default     = {}
}

variable "lambda_function_vpc_subnet_ids" {
  description = "List of subnet ids when Lambda Function should run in the VPC. Usually private or intra subnets."
  type        = list(string)
  default     = null
}

variable "lambda_function_vpc_security_group_ids" {
  description = "List of security group ids when Lambda Function should run in the VPC."
  type        = list(string)
  default     = null
}

variable "lambda_function_store_on_s3" {
  description = "Whether to store produced artifacts on S3 or locally."
  type        = bool
  default     = false
}

variable "lambda_function_s3_bucket" {
  description = "S3 bucket to store artifacts"
  type        = string
  default     = null
}

variable "lambda_function_ephemeral_storage_size" {
  description = "Amount of ephemeral storage (/tmp) in MB your Lambda Function can use at runtime. Valid value between 512 MB to 10,240 MB (10 GB)."
  type        = number
  default     = 512
}

variable "sns_topic_tags" {
  description = "Additional tags for the SNS topic"
  type        = map(string)
  default     = {}
}

variable "cloudwatch_log_group_tags" {
  description = "Additional tags for the Cloudwatch log group"
  type        = map(string)
  default     = {}
}

variable "subscription_filter_policy" {
  description = "(Optional) A valid filter policy that will be used in the subscription to filter messages seen by the target resource."
  type        = string
  default     = null
}

variable "subscription_filter_policy_scope" {
  description = "(Optional) A valid filter policy scope MessageAttributes|MessageBody"
  type        = string
  default     = null
}
