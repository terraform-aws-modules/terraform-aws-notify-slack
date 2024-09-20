locals {
  create_sns_feedback_role = local.create && var.create_sns_topic && var.enable_sns_topic_delivery_status_logs && var.sns_topic_lambda_feedback_role_arn == ""
}

data "aws_iam_policy_document" "sns_feedback" {
  count = local.create_sns_feedback_role ? 1 : 0

  statement {
    sid    = "SnsAssume"
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
      "sts:TagSession",
    ]

    principals {
      type        = "Service"
      identifiers = ["sns.amazonaws.com"]
    }
  }
}

// See https://repost.aws/knowledge-center/monitor-sns-texts-cloudwatch for required permissions to deliver status logs
data "aws_iam_policy_document" "sns_feedback_allow_log_creation" {
  count = local.create_sns_feedback_role ? 1 : 0

  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:PutMetricFilter",
      "logs:PutRetentionPolicy",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role" "sns_feedback_role" {
  count = local.create_sns_feedback_role ? 1 : 0

  name                  = var.sns_topic_feedback_role_name
  description           = var.sns_topic_feedback_role_description
  path                  = var.sns_topic_feedback_role_path
  force_detach_policies = var.sns_topic_feedback_role_force_detach_policies
  permissions_boundary  = var.sns_topic_feedback_role_permissions_boundary
  assume_role_policy    = data.aws_iam_policy_document.sns_feedback[0].json

  tags = merge(
    var.tags,
    var.sns_topic_feedback_role_tags,
  )
}

resource "aws_iam_role_policy" "sns_feedback_role" {
  count = local.create_sns_feedback_role ? 1 : 0

  role   = aws_iam_role.sns_feedback_role[0].name
  name   = "allow-cloudwatch-log-delivery"
  policy = data.aws_iam_policy_document.sns_feedback_allow_log_creation[0].json
}
