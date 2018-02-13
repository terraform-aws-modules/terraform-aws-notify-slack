data "aws_iam_policy_document" "assume_role" {
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

  statement {
    sid = "${var.kms_key_arn == "" ? "This statement has no effect" : "AllowKMSDecrypt"}"

    effect = "Allow"

    actions = ["${var.kms_key_arn == "" ? "" : "kms:Decrypt"}"]

    resources = ["${var.kms_key_arn}"]
  }
}

resource "aws_iam_role" "lambda" {
  name_prefix        = "lambda-"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role.json}"
}

resource "aws_iam_role_policy" "lambda" {
  name_prefix = "lambda-policy-"
  role        = "${aws_iam_role.lambda.id}"

  policy = "${data.aws_iam_policy_document.lambda.json}"
}
