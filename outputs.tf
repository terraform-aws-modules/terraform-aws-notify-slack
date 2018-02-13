//output "this_slack_topic_name" {
//  description = "The name of the created SNS topic for Slack"
//}

output "this_slack_topic_arn" {
  description = "The ARN of the created SNS topic from which messages will be sent to Slack"
  value       = "${local.sns_topic_arn}"
}

output "lambda_iam_role_arn" {
  description = "The ARN of the IAM role used by Lambda function"
  value       = "${aws_iam_role.lambda.arn}"
}

output "lambda_iam_role_name" {
  description = "The name of the IAM role used by Lambda function"
  value       = "${aws_iam_role.lambda.arn}"
}

output "notify_slack_lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = "${aws_lambda_function.notify_slack.arn}"
}

output "notify_slack_lambda_function_invoke_arn" {
  description = "The ARN to be used for invoking Lambda function from API Gateway"
  value       = "${aws_lambda_function.notify_slack.invoke_arn}"
}

output "notify_slack_lambda_function_last_modified" {
  description = "The date Lambda function was last modified"
  value       = "${aws_lambda_function.notify_slack.last_modified}"
}

output "notify_slack_lambda_function_version" {
  description = "Latest published version of your Lambda function"
  value       = "${aws_lambda_function.notify_slack.version}"
}
