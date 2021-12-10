# Slack Notify Lambda Functions

## Conventions

The following tools and conventions are used within this project:

- [pipenv](https://github.com/pypa/pipenv) for managing Python dependencies and development virtualenv
- [flake8](https://github.com/PyCQA/flake8) & [radon](https://github.com/rubik/radon) for linting and static code analysis
- [isort](https://github.com/timothycrosley/isort) for import statement formatting
- [black](https://github.com/ambv/black) for code formatting
- [mypy](https://github.com/python/mypy) for static type checking
- [pytest](https://github.com/pytest-dev/pytest) and [snapshottest](https://github.com/syrusakbary/snapshottest) for unit testing and snapshot testing

## Getting Started

The following instructions will help you get setup for local development and testing purposes.

### Prerequisites

#### [Pipenv](https://github.com/pypa/pipenv)

Pipenv is used to help manage the python dependencies and local virtualenv for local testing and development. To install `pipenv` please refer to the project [installation documentation](https://github.com/pypa/pipenv#installation).

Install the projects Python dependencies (with development dependencies) locally by running the following command.

```bash
  $ pipenv install --dev
```

If you add/change/modify any of the Pipfile dependencies, you can update your local virtualenv using:

```bash
  $ pipenv update
```

### Testing

#### Sample Payloads

In the `functions/` directory there are two folders that contain sample message payloads used for testing and validation:

1. `functions/events/` contains raw events as provided by AWS. You can see a more in-depth list of example events in the (AWS documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html)
2. `functions/messages/` contains SNS message payloads in the form that they are delivered to the Slack notify lambda function. The `Message` attribute field is where the payload is stored that will be parsed and sent to Slack; this can be events like those described above in #1, or any string/stringified-JSON

#### Unit Tests

There are a number of pipenv scripts that are provided to aid in testing and ensuring the codebase is formatted properly.

- `pipenv run test`: execute unit tests defined using pytest and show test coverage
- `pipenv run lint`: show linting errors and static analysis of codebase
- `pipenv run format`: auto-format codebase according to configurations provided
- `pipenv run imports`: auto-format import statements according to configurations provided
- `pipenv run typecheck`: show typecheck analysis of codebase

See the `[scripts]` section of the `Pipfile` for the complete list of script commands.

#### Snapshot Testing

Snapshot testing is used to compare a set of given inputs to generated output snapshots to aid in unit testing. The tests are run in conjunction with the standard unit tests and the output will be shown in the cumulative output from `pipenv run test`. In theory, however, the snapshots themselves should not change unless:

1. The expected output of the message payload has changed
2. Event/message payloads have been added to or removed from the project

When a change is required to update the snapshots, please do the following:

1. Update the snapshots by running:

```bash
  $ pipenv run test:updatesnapshots
  $ pipenv run format # this is necessary since the generated code follows its own style
```

2. Provide a clear reasoning within your pull request as to why the snapshots have changed

#### Integration Tests

Integration tests require setting up a live Slack webhook

To run the unit tests:

1.  Set up a dedicated slack channel as a test sandbox with it's own webhook. See [Slack Incoming Webhooks docs](https://api.slack.com/messaging/webhooks) for details.
2.  From within the `examples/notify-slack-simple/` directory, update the `slack_*` variables to use your values:

```hcl
  slack_webhook_url = "https://hooks.slack.com/services/AAA/BBB/CCC"
  slack_channel     = "aws-notification"
  slack_username    = "reporter"
```

3. Deploy the resources in the `examples/notify-slack-simple/` project using Terraform

```bash
  $ terraform init && terraform apply -y
```

4.  From within the `functions/` directory, execute the integration tests locally:

```bash
  $ pipenv run python integration_test.py
```

Within the Slack channel that is associated to the webhook URL provided, you should see all of the messages arriving. You can compared the messages to the payloads in the `functions/events/` and `functions/messages` directories; there should be one Slack message per event payload/file.

5. Do not forget to clean up your provisioned resources by returning to the `example/notify-slack-simple/` directory and destroying using Terraform:

```bash
  $ terraform destroy -y
```

## Supporting Additional Events

To add new events with custom message formatting, the general workflow will consist of (ignoring git actions for brevity):

1. Add a new example event paylod to the `functions/events/` directory; please name the file, using snake casing, in the form `<service>_<event_type>.json` such as `guardduty_finding.json` or `cloudwatch_alarm.json`
2. In the `functions/notify_slack.py` file, add the new formatting function, following a similar naming pattern like in step #1 where the function name is `format_<service>_<event_type>()` such as `format_guardduty_finding()` or `format_cloudwatch_alarm()`
3. (Optional) Ff there are different "severity" type levels that are to be mapped to Slack message color bars, create an enum that maps the possible serverity values to the appropriate colors. See the `CloudWatchAlarmState` and `GuardDutyFindingSeverity` for examples. The enum name should follow pascal case, Python standard, in the form of `<service><event_type><attribute_field>`
4. Update the snapshots to include your new event payload and expected output. Note - the other snapshots should not be affected by your change, the snapshot diff should only show your new event:

```bash
  $ pipenv run test:updatesnapshots
  $ pipenv run format # this is necessary since the generated code follows its own style
```
