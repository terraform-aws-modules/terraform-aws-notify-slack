# Change Log

All notable changes to this project will be documented in this file.

<a name="unreleased"></a>
## [Unreleased]


<a name="v2.13.0"></a>
## [v2.13.0] - 2020-03-19


<a name="v2.12.0"></a>
## [v2.12.0] - 2020-03-19


<a name="v2.11.0"></a>
## [v2.11.0] - 2020-03-19

- Add subsription filter policy support ([#74](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/74))


<a name="v2.10.0"></a>
## [v2.10.0] - 2020-01-21

- Updated CHANGELOG
- Updated pre-commit-terraform with terraform-docs 0.8.0 support ([#65](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/65))


<a name="v2.9.0"></a>
## [v2.9.0] - 2020-01-16

- Fix empty tuple error ([#64](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/64))


<a name="v2.8.0"></a>
## [v2.8.0] - 2019-12-21

- Added lambda description and improved Lambda IAM policy for KMS ([#56](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/56))


<a name="v2.7.0"></a>
## [v2.7.0] - 2019-12-20

- Added support for multiline messages ([#55](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/55))


<a name="v2.6.0"></a>
## [v2.6.0] - 2019-12-20

- Added pytest and logging (based on [#27](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/27)) ([#54](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/54))


<a name="v2.5.0"></a>
## [v2.5.0] - 2019-12-20

- Updated formatting
- use 0.12 syntax for depends_on ([#51](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/51))


<a name="v2.4.0"></a>
## [v2.4.0] - 2019-12-10

- Use urllib.parse.quote for the alarm name ([#35](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/35))
- Updated simple example a bit
- Create AWS Cloudwatch log group and give explicit access to it ([#40](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/40))
- Added support for reserved_concurrent_executions
- Updated docs, python3.7
- Add support for resource tagging ([#45](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/45))
- Upgraded module to support Terraform 0.12 ([#36](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/36))


<a name="v1.14.0"></a>
## [v1.14.0] - 2019-11-08

- Updated pre-commit hooks
- Reduce scope of IAM Policy for CloudWatch Logs ([#44](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/44))


<a name="v2.3.0"></a>
## [v2.3.0] - 2019-11-08

- Create AWS Cloudwatch log group and give explicit access to it ([#40](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/40))


<a name="v2.2.0"></a>
## [v2.2.0] - 2019-11-08

- Added support for reserved_concurrent_executions


<a name="v2.1.0"></a>
## [v2.1.0] - 2019-11-08

- Updated docs, python3.7
- Add support for resource tagging ([#45](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/45))


<a name="v2.0.0"></a>
## [v2.0.0] - 2019-06-12

- Upgraded module to support Terraform 0.12 ([#36](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/36))


<a name="v1.13.0"></a>
## [v1.13.0] - 2019-02-22

- need to convert from json string to dict when extracting message from event ([#30](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/30))


<a name="v1.12.0"></a>
## [v1.12.0] - 2019-02-21

- Pass the subject ot default_notification ([#29](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/29))


<a name="v1.11.0"></a>
## [v1.11.0] - 2018-12-28

- No longer parsing the SNS event as incoming JSON ([#23](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/23))


<a name="v1.10.0"></a>
## [v1.10.0] - 2018-08-20

- Fixed bug which causes apply failure when create = false ([#19](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/19))


<a name="v1.9.0"></a>
## [v1.9.0] - 2018-06-21

- Allow computed KMS key value (fixed [#10](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/10)) ([#18](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/18))


<a name="v1.8.0"></a>
## [v1.8.0] - 2018-06-20

- include short alarm name in slack notification text ([#14](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/14))


<a name="v1.7.0"></a>
## [v1.7.0] - 2018-06-20

- Renamed enable to create, minor fixes after [#15](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/15)
- Add flag to enable/disable creation of resources ([#15](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/15))


<a name="v1.6.0"></a>
## [v1.6.0] - 2018-06-19

- Fixed formatting
- Fix Lambda path in shared state ([#17](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/17))
- Fixed spelling a bit
- Cirumvent TF's path.module limitation for lambda filenames
- Cirumvent TF's path.module limitation for lambda filenames
- Cirumvent TF's path.module limitation for lambda filenames


<a name="v1.5.0"></a>
## [v1.5.0] - 2018-06-06

- Fixed formatting (ran 'pre-commit run -a')
- Add in slack emoji support ([#11](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/11))
- Update comments in examples/ about aws_kms_ciphertext ([#12](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/12))


<a name="v1.4.0"></a>
## [v1.4.0] - 2018-06-05

- Ignore `last_modified` timestamp deciding whether to do an update ([#9](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/9))
- Updated formatting in examples


<a name="v1.3.0"></a>
## [v1.3.0] - 2018-05-29

- Ignore changes in filename (fixed [#6](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/6))


<a name="v1.2.0"></a>
## [v1.2.0] - 2018-05-16

- Added pre-commit hook to autogenerate terraform-docs ([#7](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/7))


<a name="v1.1.0"></a>
## [v1.1.0] - 2018-03-22

- Feature/lambda function name variable ([#5](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/5))


<a name="v1.0.1"></a>
## [v1.0.1] - 2018-02-22

- Fix mismatch in alarm state labels and values ([#4](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/4))


<a name="v1.0.0"></a>
## [v1.0.0] - 2018-02-15

- Added better code, examples, docs ([#2](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/2))


<a name="v0.0.1"></a>
## v0.0.1 - 2018-02-12

- Add encrypted webhook URL example
- Fix decryption of webhook URL
- Update readme
- Add basic example
- Make KMS optional
- Add README description
- Add preliminary cloudwatch event handling lambda
- Initial commit


[Unreleased]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.13.0...HEAD
[v2.13.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.12.0...v2.13.0
[v2.12.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.11.0...v2.12.0
[v2.11.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.10.0...v2.11.0
[v2.10.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.9.0...v2.10.0
[v2.9.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.8.0...v2.9.0
[v2.8.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.7.0...v2.8.0
[v2.7.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.6.0...v2.7.0
[v2.6.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.5.0...v2.6.0
[v2.5.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.4.0...v2.5.0
[v2.4.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.14.0...v2.4.0
[v1.14.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.3.0...v1.14.0
[v2.3.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.2.0...v2.3.0
[v2.2.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.1.0...v2.2.0
[v2.1.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.0.0...v2.1.0
[v2.0.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.13.0...v2.0.0
[v1.13.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.12.0...v1.13.0
[v1.12.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.11.0...v1.12.0
[v1.11.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.10.0...v1.11.0
[v1.10.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.9.0...v1.10.0
[v1.9.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.8.0...v1.9.0
[v1.8.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.7.0...v1.8.0
[v1.7.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.6.0...v1.7.0
[v1.6.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.5.0...v1.6.0
[v1.5.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.4.0...v1.5.0
[v1.4.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.3.0...v1.4.0
[v1.3.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.2.0...v1.3.0
[v1.2.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.1.0...v1.2.0
[v1.1.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.0.1...v1.1.0
[v1.0.1]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v1.0.0...v1.0.1
[v1.0.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v0.0.1...v1.0.0
