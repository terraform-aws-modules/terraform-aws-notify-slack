# CloudWatch alerts to Slack

Configuration in this directory creates an SNS topic that sends messages to a Slack channel with Slack webhook URL encrypted using KMS and a CloudWatch Alarm that monitors the duration of lambda execution.

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

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| kms_key_arn |  | string | `arn:aws:kms:eu-west-1:000014191260:key/66db1c5d-d42b-4e28-8efb-07a9cf607a73` | no |

## Outputs

| Name | Description |
|------|-------------|
| this_sns_topic_arn | The ARN of the created SNS topic from which messages will be sent to Slack |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
