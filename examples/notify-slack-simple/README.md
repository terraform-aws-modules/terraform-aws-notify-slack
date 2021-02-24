Basic Slack notification
========================

Configuration in this directory creates an SNS topic that sends messages to a Slack channel.

Note, this example does not use KMS key.

Usage
=====

To run this example you need to execute:

```bash
$ terraform init
$ terraform plan
$ terraform apply
```

Note that this example may create resources which can cost money (AWS Elastic IP, for example). Run `terraform destroy` when you don't need these resources.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.13.0 |
| aws | >= 2.35 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 2.35 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| notify_slack | ../../ |  |

## Resources

| Name |
|------|
| [aws_sns_topic](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic) |

## Inputs

No input.

## Outputs

| Name | Description |
|------|-------------|
| lambda\_cloudwatch\_log\_group\_arn | The Amazon Resource Name (ARN) specifying the log group |
| lambda\_iam\_role\_arn | The ARN of the IAM role used by Lambda function |
| lambda\_iam\_role\_name | The name of the IAM role used by Lambda function |
| notify\_slack\_lambda\_function\_arn | The ARN of the Lambda function |
| notify\_slack\_lambda\_function\_invoke\_arn | The ARN to be used for invoking Lambda function from API Gateway |
| notify\_slack\_lambda\_function\_last\_modified | The date Lambda function was last modified |
| notify\_slack\_lambda\_function\_name | The name of the Lambda function |
| notify\_slack\_lambda\_function\_version | Latest published version of your Lambda function |
| this\_sns\_topic\_arn | The ARN of the SNS topic from which messages will be sent to Slack |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
