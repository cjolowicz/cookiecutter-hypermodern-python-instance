# Contributing

Thank you for your interest in improving this project.
This project is open-source under the [MIT License](https://opensource.org/licenses/MIT) and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md).
By participating in this project you agree to abide by its terms.

- [Source Code](https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance)
- [Documentation](https://cookiecutter-hypermodern-python-instance.readthedocs.io/)
- [Issue Tracker](https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/issues)

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
and are written using the [Pytest](https://pytest.readthedocs.io/) testing framework.

## How to submit changes

Please open a
[Pull Request](https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/pulls)
to submit changes to this project.

- Changes must be fully covered by unit tests.
- Do not forget to update the documentation, where appropriate.
- Follow [Black](https://black.readthedocs.io/) code style.

You can ensure that your changes adhere to the code style by reformatting with Black:

```sh
$ nox --session=black
```

## How to accept changes

*You need to be a project maintainer to accept changes.*

Before accepting a pull request, go through the following checklist:

- The PR must pass all checks.
- The PR must have a descriptive title.
- The PR should be labelled with the kind of change (see below).

Release notes are pre-filled with titles and authors of merged pull requests.
Labels group the pull requests into sections:

- :boom: Breaking Changes (`breaking`)
- :beetle: Fixes (`bug`)
- :package: Build System and Dependencies (`build`)
- :construction_worker: Continuous Integration (`ci`)
- :books: Documentation (`documentation`)
- :rocket: Features (`enhancement`)
- :racehorse: Performance (`performance`)
- :hammer: Refactoring (`refactoring`)
- :fire: Removals and Deprecations (`removal`)
- :lipstick: Style (`style`)
- :rotating_light: Testing (`testing`)

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
