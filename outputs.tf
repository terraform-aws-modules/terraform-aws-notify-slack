output "this_slack_topic_arn" {
  description = "The ARN of the SNS topic from which messages will be sent to Slack"
  value       = local.sns_topic_arn
}

output "lambda_iam_role_arn" {
  description = "The ARN of the IAM role used by Lambda function"
  value       = module.lambda.lambda_role_arn
}

output "lambda_iam_role_name" {
  description = "The name of the IAM role used by Lambda function"
  value       = module.lambda.lambda_role_name
}

output "notify_slack_lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = module.lambda.this_lambda_function_arn
}

output "notify_slack_lambda_function_name" {
  description = "The name of the Lambda function"
  value       = module.lambda.this_lambda_function_name
}

output "notify_slack_lambda_function_invoke_arn" {
  description = "The ARN to be used for invoking Lambda function from API Gateway"
  value       = module.lambda.this_lambda_function_invoke_arn
}

output "notify_slack_lambda_function_last_modified" {
  description = "The date Lambda function was last modified"
  value       = module.lambda.this_lambda_function_last_modified
}

output "notify_slack_lambda_function_version" {
  description = "Latest published version of your Lambda function"
  value       = module.lambda.this_lambda_function_version
}

output "lambda_cloudwatch_log_group_arn" {
  description = "The Amazon Resource Name (ARN) specifying the log group"
  value       = element(concat(aws_cloudwatch_log_group.lambda.*.arn, [""]), 0)
}
