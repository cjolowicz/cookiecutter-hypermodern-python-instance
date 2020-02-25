# Contributing

Thank you for your interest in improving this project.
This project is open-source under the [MIT License](https://opensource.org/licenses/MIT) and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code](https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance)
- [Documentation](https://cookiecutter-hypermodern-python-instance.readthedocs.io/)
- [Issue Tracker](https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/issues)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## How to report a bug

Report bugs on the [Issue Tracker](https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/issues).

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Issue Tracker](https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/issues).

## How to set up your development environment

You need Python 3.6+ and the following tools:

- [Poetry](https://python-poetry.org/)
- [Nox](https://nox.thea.codes/)

Install the package with development requirements:

```sh
$ poetry install
```

You can now run an interactive Python session,
development tools,
or the command-line interface
using [poetry run](https://python-poetry.org/docs/cli/#run):

```sh
$ poetry run python
$ poetry run cookiecutter-hypermodern-python-instance
```

## How to test the project

Run the full test suite:

```sh
$ nox
```

List the available Nox sessions:

```sh
$ nox --list-sessions
```

You can also run a specific Nox session.
For example, invoke the unit test suite like this:

```sh
$ nox --session=tests
```

Unit tests are located in the `tests` directory,
and are written using the [pytest](https://pytest.readthedocs.io/) testing framework.

## How to submit changes

Open a [pull request](https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/pulls)
to submit changes to this project.
Please check that your pull request meets these guidelines:

- Pull requests must include unit tests. This project maintains 100% test coverage.
- If the pull request adds functionality, the documentation should be updated.
- Follow [Black](https://black.readthedocs.io/) code style.

You can ensure that your changes adhere to the code style by reformatting with Black:

```sh
$ nox --session=black
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

## How to accept changes

*You need to be a project maintainer to accept changes.*

Before accepting a pull request, go through the following checklist:

- The PR must pass all checks.
- The PR must have a descriptive title.
- The PR should be labelled with the kind of change (see below).

Release notes are pre-filled with titles and authors of merged pull requests.
Labels group the pull requests into sections.
The following list shows the available sections,
with associated labels in parentheses:

- 💥 Breaking Changes (`breaking`)
- 🚀 Features (`enhancement`)
- 🔥 Removals and Deprecations (`removal`)
- 🐞 Fixes (`bug`)
- 🐎 Performance (`performance`)
- 🚨 Testing (`testing`)
- 👷 Continuous Integration (`ci`)
- 📚 Documentation (`documentation`)
- 🔨 Refactoring (`refactoring`)
- 💄 Style (`style`)
- 📦 Build System and Dependencies (`build`)

## How to make a release

*You need to be a project maintainer to make a release.*

Before making a release, go through the following checklist:

- The master branch passes all checks.
- The development release on [TestPyPI](https://test.pypi.org/project/cookiecutter-hypermodern-python-instance) looks good.
- All PRs for the release have been merged.

Making a release is a two-step process:

1. Bump the version using [poetry version](https://python-poetry.org/docs/cli/#version). (Commit and push.)
2. Publish a GitHub Release.

When bumping the version,
adhere to [Semantic Versioning](https://semver.org/) and
[PEP 440](https://www.python.org/dev/peps/pep-0440/).

A draft release is being maintained based on merged pull requests.
To publish the release, follow these steps:

1. Click **Edit** next to the draft release.
2. Enter a tag of the form `v<version>`, using the new project version.
3. Enter the release title, e.g. `<version>`.
4. Edit the release description, if required.
5. Click **Publish Release**.

After publishing the release, the following automated steps are triggered:

- The Git tag is applied to the repository.
- The Release workflow on GitHub Actions triggers the PyPI upload.
- Read the Docs builds a new stable version of the documentation.
