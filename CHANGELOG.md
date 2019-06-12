<a name="unreleased"></a>
## [Unreleased]



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

- Merge pull request [#1](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/1) from nazartm/cloudwatch-event
- Add encrypted webhook URL example
- Fix decryption of webhook URL
- Update readme
- Add basic example
- Make KMS optional
- Add README description
- Add preliminary cloudwatch event handling lambda
- Initial commit


[Unreleased]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.0.0...HEAD
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
