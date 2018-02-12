Slack notification with KMS encrypted webhook URL
=================================================

Configuration in this directory creates an SNS topic that sends messages to a Slack channel with Slack webhook URL encrypted using KMS.

Usage
=====

To run this example you need to execute:

```bash
$ terraform init
$ terraform plan
$ terraform apply
```

Note that in practice, encryption of the Slack webhook URL should happend differently.

Note that this example may create resources which can cost money (AWS Elastic IP, for example). Run `terraform destroy` when you don't need these resources.