# CloudWatch alerts to Slack

Configuration in this directory creates a VPC, an SNS topic that sends messages to a Slack channel with Slack webhook URL encrypted using KMS and a CloudWatch Alarm that monitors the duration of lambda execution.

## KMS keys

There are 3 ways to define KMS key which should be used by Lambda function:

1. Create [aws_kms_key resource](https://www.terraform.io/docs/providers/aws/r/kms_key.html) and put ARN of it as `kms_key_arn` argument to this module
1. Use [aws_kms_alias data-source](https://www.terraform.io/docs/providers/aws/d/kms_alias.html) to get an existing KMS key alias and put ARN of it as `kms_key_arn` argument to this module
1. Hard-code the ARN of KMS key

### Option 1:

```hcl
resource "aws_kms_key" "this" {
  description = "KMS key for notify-slack test"
}

resource "aws_kms_alias" "this" {
  name          = "alias/kms-test-key"
  target_key_id = aws_kms_key.this.id
}

// kms_key_arn = aws_kms_key.this.arn
```

### Option 2:

```
data "aws_kms_alias" "this" {
 name = "alias/kms-test-key"
}

// kms_key_arn = data.aws_kms_alias.this.target_key_arn
```

### Option 3:

```
// kms_key_arn = "arn:aws:kms:eu-west-1:835367859851:key/054b4846-95fe-4537-94f2-1dfd255238cf"
```

## Usage

To run this example you need to execute:

```bash
$ terraform init
$ terraform plan
$ terraform apply
```

Note that in practice, encryption of the Slack webhook URL should happen differently (outside of this module).

Note that this example may create resources which can cost money. Run `terraform destroy` when you don't need these resources.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.13.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 2.35 |
| <a name="requirement_random"></a> [random](#requirement\_random) | >= 2 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 2.35 |
| <a name="provider_random"></a> [random](#provider\_random) | >= 2 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_notify_slack"></a> [notify\_slack](#module\_notify\_slack) | ../../ |  |
| <a name="module_vpc"></a> [vpc](#module\_vpc) | terraform-aws-modules/vpc/aws |  |

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_metric_alarm.lambda_duration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_kms_ciphertext.slack_url](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_ciphertext) | resource |
| [aws_kms_key.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_key) | resource |
| [random_pet.this](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/pet) | resource |

## Inputs

No inputs.

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lambda_iam_role_arn"></a> [lambda\_iam\_role\_arn](#output\_lambda\_iam\_role\_arn) | The ARN of the IAM role used by Lambda function |
| <a name="output_lambda_iam_role_name"></a> [lambda\_iam\_role\_name](#output\_lambda\_iam\_role\_name) | The name of the IAM role used by Lambda function |
| <a name="output_notify_slack_lambda_function_arn"></a> [notify\_slack\_lambda\_function\_arn](#output\_notify\_slack\_lambda\_function\_arn) | The ARN of the Lambda function |
| <a name="output_notify_slack_lambda_function_invoke_arn"></a> [notify\_slack\_lambda\_function\_invoke\_arn](#output\_notify\_slack\_lambda\_function\_invoke\_arn) | The ARN to be used for invoking Lambda function from API Gateway |
| <a name="output_notify_slack_lambda_function_last_modified"></a> [notify\_slack\_lambda\_function\_last\_modified](#output\_notify\_slack\_lambda\_function\_last\_modified) | The date Lambda function was last modified |
| <a name="output_notify_slack_lambda_function_name"></a> [notify\_slack\_lambda\_function\_name](#output\_notify\_slack\_lambda\_function\_name) | The name of the Lambda function |
| <a name="output_notify_slack_lambda_function_version"></a> [notify\_slack\_lambda\_function\_version](#output\_notify\_slack\_lambda\_function\_version) | Latest published version of your Lambda function |
| <a name="output_this_sns_topic_arn"></a> [this\_sns\_topic\_arn](#output\_this\_sns\_topic\_arn) | The ARN of the SNS topic from which messages will be sent to Slack |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
