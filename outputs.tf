output "this_slack_topic_arn" {
  description = "The ARN of the SNS topic from which messages will be sent to Slack"
  value       = local.sns_topic_arn
}

output "lambda_iam_role_arn" {
  description = "The ARN of the IAM role used by Lambda function"
  value       = element(concat(aws_iam_role.lambda.*.arn, [""]), 0)
}

output "lambda_iam_role_name" {
  description = "The name of the IAM role used by Lambda function"
  value       = element(concat(aws_iam_role.lambda.*.arn, [""]), 0)
}

output "notify_slack_lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = element(concat(aws_lambda_function.notify_slack.*.arn, [""]), 0)
}

output "notify_slack_lambda_function_name" {
  description = "The name of the Lambda function"
  value = element(
    concat(aws_lambda_function.notify_slack.*.function_name, [""]),
    0,
  )
}

output "notify_slack_lambda_function_invoke_arn" {
  description = "The ARN to be used for invoking Lambda function from API Gateway"
  value = element(
    concat(aws_lambda_function.notify_slack.*.invoke_arn, [""]),
    0,
  )
}

output "notify_slack_lambda_function_last_modified" {
  description = "The date Lambda function was last modified"
  value = element(
    concat(aws_lambda_function.notify_slack.*.last_modified, [""]),
    0,
  )
}

output "notify_slack_lambda_function_version" {
  description = "Latest published version of your Lambda function"
  value       = element(concat(aws_lambda_function.notify_slack.*.version, [""]), 0)
}

