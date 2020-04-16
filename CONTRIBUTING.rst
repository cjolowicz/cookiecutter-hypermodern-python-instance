Contributor Guide
=================

Thank you for your interest in improving this project. This project is
open-source under the `MIT
License <https://opensource.org/licenses/MIT>`__ and welcomes
contributions in the form of bug reports, feature requests, and pull
requests.

Here is a list of important resources for contributors:

-  `Source
   Code <https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance>`__
-  `Documentation <https://cookiecutter-hypermodern-python-instance.readthedocs.io/>`__
-  `Issue
   Tracker <https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/issues>`__
-  `Code of
   Conduct <https://cookiecutter-hypermodern-python-instance.readthedocs.io/codeofconduct.html>`__

How to report a bug
-------------------

Report bugs on the `Issue
Tracker <https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/issues>`__.

When filing an issue, make sure to answer these questions:

-  Which operating system and Python version are you using?
-  Which version of this project are you using?
-  What did you do?
-  What did you expect to see?
-  What did you see instead?

The best way to get your bug fixed is to provide a test case, and/or
steps to reproduce the issue.

How to request a feature
------------------------

Request features on the `Issue
Tracker <https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/issues>`__.

How to set up your development environment
------------------------------------------

You need Python 3.6+ and the following tools:

-  `Poetry <https://python-poetry.org/>`__
-  `Nox <https://nox.thea.codes/>`__

Install the package with development requirements:

.. code:: console

   $ poetry install

You can now run an interactive Python session, or the command-line
interface:

.. code:: console

   $ poetry run python
   $ poetry run cookiecutter-hypermodern-python-instance

How to test the project
-----------------------

Run the full test suite:

.. code:: console

   $ nox

List the available Nox sessions:

.. code:: console

   $ nox --list-sessions

You can also run a specific Nox session. For example, invoke the unit
test suite like this:

.. code:: console

   $ nox --session=tests

Unit tests are located in the ``tests`` directory, and are written using
the `pytest <https://pytest.readthedocs.io/>`__ testing framework.

How to submit changes
---------------------

Open a `pull
request <https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/pulls>`__
to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

-  The Nox test suite must pass without errors and warnings.
-  Include unit tests. This project maintains 100% code coverage.
-  If your changes add functionality, update the documentation
   accordingly.

Feel free to submit early, though—we can always iterate on this.

You can ensure that your changes adhere to the code style by
reformatting with `Black <https://black.readthedocs.io/>`__:

.. code:: console

   $ nox --session=black

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate
your approach.
