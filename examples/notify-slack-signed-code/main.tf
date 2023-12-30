provider "aws" {
  region = local.region
}

locals {
  name   = "ex-${replace(basename(path.cwd), "_", "-")}"
  region = "eu-west-1"
  tags = {
    Owner       = "user"
    Environment = "dev"
  }
  functions_path  = "../../functions"
  source_filename = "notify_slack.py"
  s3_bucket_name  = "${data.aws_caller_identity.current.account_id}-${local.name}"
}

################################################################################
# Supporting Resources
################################################################################

resource "aws_sns_topic" "example" {
  name = local.name
  tags = local.tags
}

resource "aws_s3_bucket" "example" {
  bucket        = local.s3_bucket_name
  force_destroy = true
  tags          = local.tags
}

resource "aws_s3_bucket_versioning" "example" {
  bucket = aws_s3_bucket.example.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_object" "example" {
  bucket = aws_s3_bucket.example.id
  key    = replace(data.archive_file.example.output_path, "./", "")
  source = data.archive_file.example.output_path
}

resource "aws_signer_signing_profile" "example" {
  platform_id = "AWSLambda-SHA384-ECDSA"
}

resource "aws_signer_signing_job" "example" {
  profile_name = aws_signer_signing_profile.example.name

  source {
    s3 {
      bucket  = aws_s3_bucket.example.id
      key     = aws_s3_object.example.id
      version = aws_s3_object.example.version_id
    }
  }

  destination {
    s3 {
      bucket = aws_s3_bucket.example.id
    }
  }

  ignore_signing_job_failure = false
}

resource "aws_lambda_code_signing_config" "example" {
  allowed_publishers {
    signing_profile_version_arns = [
      aws_signer_signing_profile.example.version_arn,
    ]
  }

  policies {
    untrusted_artifact_on_deployment = "Enforce"
  }
}

################################################################################
# Slack Notify Module
################################################################################

module "notify_slack" {
  source = "../../"

  sns_topic_name   = aws_sns_topic.example.name
  create_sns_topic = false

  lambda_function_code_signing_config_arn = aws_lambda_code_signing_config.example.arn
  custom_lambda_source_name               = replace(local.source_filename, ".py", "")

  s3_existing_package = {
    bucket = aws_signer_signing_job.example.signed_object[0].s3[0].bucket
    key    = aws_signer_signing_job.example.signed_object[0].s3[0].key
  }

  slack_webhook_url = "https://hooks.slack.com/services/AAA/BBB/CCC"
  slack_channel     = "aws-notification"
  slack_username    = "reporter"

  tags = local.tags
}

################################################################################
# Integration Testing Support
# This populates a file that is gitignored to aid in executing the integration tests locally
################################################################################

resource "local_file" "integration_testing" {
  filename = "${path.module}/../../functions/.int.env"
  content  = <<-EOT
    REGION=${local.region}
    LAMBDA_FUNCTION_NAME=${module.notify_slack.notify_slack_lambda_function_name}
    SNS_TOPIC_ARN=${aws_sns_topic.example.arn}
    EOT
}
