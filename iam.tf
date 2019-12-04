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

data "aws_iam_policy_document" "lambda_basic" {
  count = var.create ? 1 : 0

  statement {
    sid = "AllowWriteToCloudwatchLogs"

    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

data "aws_iam_policy_document" "lambda" {
  count = var.kms_key_arn != "" && var.create ? 1 : 0

  source_json = data.aws_iam_policy_document.lambda_basic[0].json

  statement {
    sid = "AllowKMSDecrypt"

    effect = "Allow"

    actions = ["kms:Decrypt"]

    resources = [var.kms_key_arn]
  }
}

data "aws_iam_policy_document" "lambda_xray" {
  sid = "AllowXRay"

  effect = "Allow"

  actions = [
    "xray:PutTraceSegments",
    "xray:PutTelemetryRecords",
    "xray:GetSamplingRules",
    "xray:GetSamplingTargets",
    "xray:GetSamplingStatisticSummaries",
  ]

  principals {
    identifiers = ["lambda.amazonaws.com"]
    type        = "Service"
  }
}

resource "aws_iam_role" "lambda" {
  count = var.create ? 1 : 0

  name_prefix        = "lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role[0].json
}

resource "aws_iam_role_policy" "lambda" {
  count = var.create ? 1 : 0

  name_prefix = "lambda-policy-"
  role        = aws_iam_role.lambda[0].id

  policy = element(
    concat(
      data.aws_iam_policy_document.lambda.*.json,
      data.aws_iam_policy_document.lambda_basic.*.json,
      data.aws_iam_policy_document.lambda_xray.*.json,
    ),
    0,
  )
}

