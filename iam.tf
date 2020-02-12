locals {
  lambda_policy_document = [{
    sid    = "AllowWriteToCloudwatchLogs"
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = [
      element(concat(aws_cloudwatch_log_group.notify_lambda[*].arn, list("")), 0),
      element(concat(aws_cloudwatch_log_group.approve_request_lambda[*].arn, list("")), 0),
      element(concat(aws_cloudwatch_log_group.approve_response_lambda[*].arn, list("")), 0)
    ]
  }]

  lambda_policy_document_kms = var.kms_key_arn != "" ? [{
    sid       = "AllowKMSDecrypt"
    effect    = "Allow"
    actions   = ["kms:Decrypt"]
    resources = [var.kms_key_arn]
  }] : []
}

data "aws_iam_policy_document" "assume_role" {
  count = var.create ? 1 : 0

  statement {
    effect = "Allow"

    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda" {
  count = var.create ? 1 : 0

  dynamic "statement" {
    for_each = concat(local.lambda_policy_document, local.lambda_policy_document_kms)
    content {
      sid       = statement.value.sid
      effect    = statement.value.effect
      actions   = statement.value.actions
      resources = statement.value.resources
    }
  }
}

resource "aws_iam_role" "lambda" {
  count = var.create ? 1 : 0

  name_prefix        = "lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role[0].json

  tags = merge(var.tags, var.iam_role_tags)
}

resource "aws_iam_role_policy" "lambda" {
  count = var.create ? 1 : 0

  name_prefix = "lambda-policy-"
  role        = aws_iam_role.lambda[0].id
  policy      = data.aws_iam_policy_document.lambda[0].json
}
