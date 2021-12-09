# Slack Notify Lambda Functions

## Conventions

The following tools and conventions are used within this project:

- [pipenv](https://github.com/pypa/pipenv) for managing Python dependencies and development virtualenv
- [flake8](https://github.com/PyCQA/flake8) & [radon](https://github.com/rubik/radon) for linting and static code analysis
- [isort](https://github.com/timothycrosley/isort) for import statement formatting
- [black](https://github.com/ambv/black) for code formatting

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

#### Unit Tests

There are a number of pipenv scripts that are provided to aid in testing and ensuring the codebase is formatted properly.

- `pipenv run test`: execute unit tests defined using pytest and show test coverage
- `pipenv run lint`: show linting errors and static analysis of codebase
- `pipenv run format`: auto-format codebase according to configurations provided
- `pipenv run imports`: auto-format import statements according to configurations provided
- `pipenv run typecheck`: show typecheck analysis of codebase

See the `[scripts]` section of the `Pipfile` for the complete list of script commands.

#### Integration Tests

Integration tests require setting up a live Slack webhook

To run the unit tests:

1.  Set up a dedicated slack channel as a test sandbox with it's own webhook. See [Slack Incoming Webhooks docs](https://api.slack.com/messaging/webhooks) for details.
2.  Make a copy of the sample environment variables file

```bash
cp .envrc.sample .envrc
```

3. Update the environment variable values in the copied `.envrc` file with your values
4. Inject the environment variables into your CLI session. You can use any number of methods to do this:
  - Run `source .envrc`
  - Copy the environment variables out of the file and paste into your CLI session and hit `enter`
  - Use [`direnv`](https://direnv.net/) and execute `direnv allow`
3.  Run the tests:

```bash
  $ pipenv run test
```
