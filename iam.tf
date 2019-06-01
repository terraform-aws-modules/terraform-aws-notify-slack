data "aws_iam_policy_document" "assume_role" {
  count = var.create

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
  count = var.create

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
  count = var.create_with_kms_key == 1 ? 1 : 0 * var.create

  source_json = data.aws_iam_policy_document.lambda_basic[0].json

  statement {
    sid = "AllowKMSDecrypt"

    effect = "Allow"

    actions = ["kms:Decrypt"]

    resources = [var.kms_key_arn == "" ? "" : var.kms_key_arn]
  }
}

resource "aws_iam_role" "lambda" {
  count = var.create

  name_prefix        = "lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role[0].json
}

resource "aws_iam_role_policy" "lambda" {
  count = var.create

  name_prefix = "lambda-policy-"
  role        = aws_iam_role.lambda[0].id

  policy = element(
    compact(
      concat(
        data.aws_iam_policy_document.lambda.*.json,
        data.aws_iam_policy_document.lambda_basic.*.json,
      ),
    ),
    0,
  )
}

