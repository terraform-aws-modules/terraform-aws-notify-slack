# Changelog

All notable changes to this project will be documented in this file.

## [6.4.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v6.3.0...v6.4.0) (2024-04-24)


### Features

* Improved AWS backup notification readability ([#222](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/222)) ([27d1c46](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/27d1c464f80708740d8d155e7cb11367b41bab6c))

## [6.3.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v6.2.0...v6.3.0) (2024-04-22)


### Features

* Update Python lambda runtime from `3.8` to `3.11` ([#225](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/225)) ([b4ef4e4](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/b4ef4e45e9f3dafb774ccf62d9473b338de68f3f))

## [6.2.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v6.1.2...v6.2.0) (2024-04-22)


### Features

* Added architecture variable ([#224](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/224)) ([1ae3ab7](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/1ae3ab7e084341e7a1fd3acccb15d2971020fce5))

## [6.1.2](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v6.1.1...v6.1.2) (2024-03-26)


### Bug Fixes

* Correct assume role permissions for SNS service to assume IAM role ([#220](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/220)) ([dae0c0f](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/dae0c0f49d41cf98c5e31af7912ed406eea81c83))

## [6.1.1](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v6.1.0...v6.1.1) (2024-03-06)


### Bug Fixes

* Update CI workflow versions to remove deprecated runtime warnings ([#218](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/218)) ([44edd19](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/44edd191bac2812951faea9562c685fbeeeefee8))

## [6.1.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v6.0.0...v6.1.0) (2023-12-11)


### Features

* Expose `hash_extra` variable from Lambda module ([#211](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/211)) ([ee30bb3](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/ee30bb3f5c0da7c118c8c09fbb195a7c0e607f73))

## [6.0.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v5.6.0...v6.0.0) (2023-05-18)


### ⚠ BREAKING CHANGES

* Added variable to filter body of message on SNS level and bumped min Terraform version to 1.0 (#196)

### Features

* Added variable to filter body of message on SNS level and bumped min Terraform version to 1.0 ([#196](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/196)) ([ab660f7](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/ab660f7e86aec7a4f134036460b98eeb92c6c4c8))

## [5.6.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v5.5.0...v5.6.0) (2023-01-26)


### Features

* Add account ID to GuardDuty event notification ([#187](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/187)) ([e3452b4](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/e3452b424a0e5ccdaf69935094e9fb7785fb315b))

## [5.5.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v5.4.1...v5.5.0) (2022-12-07)


### Features

* Add SNS topic delivery status IAM role ([#178](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/178)) ([2863105](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/2863105fd6e07ea0f16500928242968c4b4873cb))

### [5.4.1](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v5.4.0...v5.4.1) (2022-11-07)


### Bug Fixes

* Update CI configuration files to use latest version ([#181](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/181)) ([6ca4605](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/6ca4605be57c4dd17c3daf87867b6e98136b0914))

## [5.4.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v5.3.0...v5.4.0) (2022-10-21)


### Features

* Add lambda dead-letter queue variables ([#180](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/180)) ([010aa89](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/010aa89147f91eeb95e7d842d90eccc3beac6265))

## [5.3.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v5.2.0...v5.3.0) (2022-06-17)


### Features

* Added support for AWS Health events ([#170](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/170)) ([3d38bfa](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/3d38bfa524541a6497ebcc77051ef78253cc4a3e))

## [5.2.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v5.1.0...v5.2.0) (2022-06-14)


### Features

* Added support for custom lambda function ([#172](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/172)) ([4a9d0b0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/4a9d0b02a9421ff52b392145aaa2aea0c7317a51))

## [5.1.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v5.0.0...v5.1.0) (2022-05-04)


### Features

* Added ephemeral_storage_size variable ([#167](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/167)) ([c82299a](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/c82299aaec22f301c62f220d8446675647168ff4))

## [5.0.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.24.0...v5.0.0) (2022-03-31)


### ⚠ BREAKING CHANGES

* - Update lambda module to 3.1.0 to support AWS provider version 4.8+

### Features

* Update lambda module to 3.1.0 to support AWS provider version 4.8+ ([#166](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/166)) ([ea822a3](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/ea822a3dbd4ac24803385cabae43538c9a3b10f3))

# [4.24.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.23.0...v4.24.0) (2021-12-14)


### Features

* Revert incorrectly removed output this_slack_topic_arn ([#159](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/159)) ([24ec027](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/24ec027e1b6fe708eb4a6d7788a64d9452ecbfe0))

# [4.23.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.22.0...v4.23.0) (2021-12-11)


### Features

* add support for recreating package locally if not missing/not present ([#158](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/158)) ([912e11d](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/912e11dc38416650ac07e0762a5e469a030032bd))

# [4.22.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.21.0...v4.22.0) (2021-12-10)


### Features

* add lint and unit test workflow checks for pull requests ([#152](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/152)) ([d2675ec](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/d2675eca91f3ca4bc8b7a18912ae84b36b7922f1))

# [4.21.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.20.0...v4.21.0) (2021-12-10)


### Features

* Added policy path variable to lambda module IAM role policy ([#153](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/153)) ([b3179a9](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/b3179a9f025943da60daf39d3ce73e88ed57e9ba))

# [4.20.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.19.0...v4.20.0) (2021-12-09)


### Features

* Update lambda module and bump Terraform/AWS provider versions ([#151](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/151)) ([0a1fae8](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/0a1fae86060248353eea2ededad26f43774e500e))

# [4.19.0](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.18.0...v4.19.0) (2021-12-09)


### Bug Fixes

* update CI/CD process to enable auto-release workflow ([#149](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/149)) ([f7dd0a3](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/f7dd0a35d1c140a3465564740abe3579c9e12b48))


### Features

* Added path input variable for lambda module IAM role ([#150](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/150)) ([fc0c120](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/commit/fc0c120bd379be65177745637ad402b46334cda5))

<a name="v4.18.0"></a>
## [v4.18.0] - 2021-10-01

- feat: Added support for GuardDuty Findings format ([#143](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/143))


<a name="v4.17.0"></a>
## [v4.17.0] - 2021-06-28

- feat: Allow custom attachement ([#123](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/123))


<a name="v4.16.0"></a>
## [v4.16.0] - 2021-06-28

- feat: add support for nested messages ([#142](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/142))


<a name="v4.15.0"></a>
## [v4.15.0] - 2021-05-25

- chore: Remove check boxes that don't render properly in module doc ([#140](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/140))
- chore: update CI/CD to use stable `terraform-docs` release artifact and discoverable Apache2.0 license ([#138](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/138))


<a name="v4.14.0"></a>
## [v4.14.0] - 2021-04-19

- feat: Updated code to support Terraform 0.15 ([#136](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/136))
- chore: update documentation and pin `terraform_docs` version to avoid future changes ([#134](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/134))


<a name="v4.13.0"></a>
## [v4.13.0] - 2021-03-12

- fix: use the current aws partition ([#133](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/133))
- chore: align ci-cd static checks to use individual minimum Terraform versions ([#131](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/131))
- fix: Remove data resource for sns topic to avoid race condition ([#81](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/81))
- chore: add ci-cd workflow for pre-commit checks ([#128](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/128))
- feat: Improve slack message formatting for generic messages ([#124](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/124))
- chore: update documentation based on latest `terraform-docs` which includes module and resource sections ([#126](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/126))
- feat: add support for GovCloud URLs ([#114](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/114))
- feat: Allow Lambda function to be VPC bound ([#122](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/122))
- feat: Updated version of terraform-aws-lambda module to 1.28.0 ([#119](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/119))
- feat: Updated version of Terraform AWS Lambda module to support multiple copies ([#117](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/117))
- fix: Typo on subscription_filter_policy variable ([#113](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/113))
- docs: Added a note about using with Terraform Cloud Agents ([#108](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/108))
- feat: allow reuse of existing lambda_role ([#85](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/85))
- fix: Fix regression with aws_cloudwatch_log_group resource after upgrade of AWS provider 3.0 ([#106](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/106))
- docs: Updated version of module to use for Terraform 0.12 users
- fix: Updated version requirements to be Terraform 0.13 only ([#101](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/101))
- feat: Updated Lambda module to work with Terraform 0.13 ([#99](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/99))
- fix: Bump version of lambda module that supports Terraform 13 and AWS Provider 3.x ([#96](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/96))


<a name="v3.6.0"></a>
## [v3.6.0] - 2021-03-01

- fix: Fix regression with aws_cloudwatch_log_group resource after upgrade of AWS provider 3.0 ([#106](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/106)) ([#130](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/130))
- feat: Updated version of Lambda module to allow AWS provider version 3


<a name="v4.12.0"></a>
## [v4.12.0] - 2021-03-01

- fix: Remove data resource for sns topic to avoid race condition ([#81](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/81))
- chore: add ci-cd workflow for pre-commit checks ([#128](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/128))


<a name="v4.11.0"></a>
## [v4.11.0] - 2021-02-21

- feat: Improve slack message formatting for generic messages ([#124](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/124))


<a name="v4.10.0"></a>
## [v4.10.0] - 2021-02-20

- chore: update documentation based on latest `terraform-docs` which includes module and resource sections ([#126](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/126))


<a name="v4.9.0"></a>
## [v4.9.0] - 2020-12-18

- feat: add support for GovCloud URLs ([#114](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/114))


<a name="v4.8.0"></a>
## [v4.8.0] - 2020-12-18

- feat: Allow Lambda function to be VPC bound ([#122](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/122))


<a name="v4.7.0"></a>
## [v4.7.0] - 2020-11-17

- feat: Updated version of terraform-aws-lambda module to 1.28.0 ([#119](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/119))


<a name="v4.6.0"></a>
## [v4.6.0] - 2020-11-05

- feat: Updated version of Terraform AWS Lambda module to support multiple copies ([#117](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/117))


<a name="v4.5.0"></a>
## [v4.5.0] - 2020-10-15

- fix: Typo on subscription_filter_policy variable ([#113](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/113))


<a name="v4.4.0"></a>
## [v4.4.0] - 2020-10-08

- docs: Added a note about using with Terraform Cloud Agents ([#108](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/108))


<a name="v4.3.0"></a>
## [v4.3.0] - 2020-09-07

- feat: allow reuse of existing lambda_role ([#85](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/85))


<a name="v4.2.0"></a>
## [v4.2.0] - 2020-09-07

- fix: Fix regression with aws_cloudwatch_log_group resource after upgrade of AWS provider 3.0 ([#106](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/106))
- docs: Updated version of module to use for Terraform 0.12 users
- fix: Updated version requirements to be Terraform 0.13 only ([#101](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/101))
- feat: Updated Lambda module to work with Terraform 0.13 ([#99](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/99))
- fix: Bump version of lambda module that supports Terraform 13 and AWS Provider 3.x ([#96](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/96))


<a name="v3.5.0"></a>
## [v3.5.0] - 2020-08-14

- feat: Updated version of Lambda module to allow AWS provider version 3


<a name="v4.1.0"></a>
## [v4.1.0] - 2020-08-14

- fix: Updated version requirements to be Terraform 0.13 only ([#101](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/101))


<a name="v4.0.0"></a>
## [v4.0.0] - 2020-08-13

- feat: Updated Lambda module to work with Terraform 0.13 ([#99](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/99))
- fix: Bump version of lambda module that supports Terraform 13 and AWS Provider 3.x ([#96](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/96))


<a name="v3.4.0"></a>
## [v3.4.0] - 2020-08-13

- feat: update required version of aws provider to allow 3.0 ([#95](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/95))


<a name="v3.3.0"></a>
## [v3.3.0] - 2020-06-19

- Updated README
- feat: Add support for SSE on the topic ([#82](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/82))


<a name="v3.2.0"></a>
## [v3.2.0] - 2020-06-11

- feat: Updated version of Lambda module


<a name="v3.1.0"></a>
## [v3.1.0] - 2020-06-10

- fix: Upgraded version of Lambda module (fix [#84](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/84))


<a name="v3.0.0"></a>
## [v3.0.0] - 2020-06-07

- Updated pre-commit hooks
- feat: Rewrote module to handle Lambda resources properly with terraform-aws-lambda module ([#83](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/83))
- chore: Removed stale.yml from .github folder
- fix: Stale bot should process only issues for now ([#79](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/79))


<a name="v2.15.0"></a>
## [v2.15.0] - 2020-04-13

- docs: Updated required versions in README
- Add support fro IAM role boundary policy ([#61](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/61))


<a name="v2.14.0"></a>
## [v2.14.0] - 2020-04-13

- docs: Updated README after [#62](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/62)
- feat: Add support for custom name prefixes for IAM role and policy ([#62](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/62))
- fix: Move stale.yml to .github ([#78](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/78))
- feat: Add Stale Bot Config ([#77](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/77))


<a name="v2.13.0"></a>
## [v2.13.0] - 2020-03-19



<a name="v2.12.0"></a>
## [v2.12.0] - 2020-03-19



<a name="v2.11.0"></a>
## [v2.11.0] - 2020-03-19

- Add subsription filter policy support ([#74](https://github.com/terraform-aws-modules/terraform-aws-notify-slack/issues/74))


<a name="v2.10.0"></a>
## [v2.10.0] - 2020-01-21

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


[Unreleased]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.18.0...HEAD
[v4.18.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.17.0...v4.18.0
[v4.17.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.16.0...v4.17.0
[v4.16.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.15.0...v4.16.0
[v4.15.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.14.0...v4.15.0
[v4.14.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.13.0...v4.14.0
[v4.13.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v3.6.0...v4.13.0
[v3.6.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.12.0...v3.6.0
[v4.12.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.11.0...v4.12.0
[v4.11.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.10.0...v4.11.0
[v4.10.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.9.0...v4.10.0
[v4.9.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.8.0...v4.9.0
[v4.8.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.7.0...v4.8.0
[v4.7.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.6.0...v4.7.0
[v4.6.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.5.0...v4.6.0
[v4.5.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.4.0...v4.5.0
[v4.4.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.3.0...v4.4.0
[v4.3.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.2.0...v4.3.0
[v4.2.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v3.5.0...v4.2.0
[v3.5.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.1.0...v3.5.0
[v4.1.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v4.0.0...v4.1.0
[v4.0.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v3.4.0...v4.0.0
[v3.4.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v3.3.0...v3.4.0
[v3.3.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v3.2.0...v3.3.0
[v3.2.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v3.1.0...v3.2.0
[v3.1.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v3.0.0...v3.1.0
[v3.0.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.15.0...v3.0.0
[v2.15.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.14.0...v2.15.0
[v2.14.0]: https://github.com/terraform-aws-modules/terraform-aws-notify-slack/compare/v2.13.0...v2.14.0
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
