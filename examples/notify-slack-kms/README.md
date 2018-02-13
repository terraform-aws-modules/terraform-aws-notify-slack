# Slack notification with KMS encrypted webhook URL

Configuration in this directory creates an SNS topic that sends messages to a Slack channel with Slack webhook URL encrypted using KMS.

## Usage

To run this example you need to execute:

```bash
$ terraform init
$ terraform plan
$ terraform apply
```

Note that in practice, encryption of the Slack webhook URL should happen differently (outside of this module).

Note that this example may create resources which can cost money. Run `terraform destroy` when you don't need these resources.
