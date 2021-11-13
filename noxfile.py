"""Nox sessions."""
import shutil
import sys
from pathlib import Path
from textwrap import dedent
from typing import Iterable

import nox

try:
    import nox_poetry.sessions
    import nox_poetry.poetry
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None


package = "cookiecutter_hypermodern_python_instance"
python_versions = ["3.10", "3.9", "3.8", "3.7"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = (
    "pre-commit",
    "safety",
    "mypy",
    "tests",
    "typeguard",
    "xdoctest",
    "docs-build",
)


def build_package(self: nox_poetry.sessions._PoetrySession) -> str:
    """Build a distribution archive for the package.

    This function uses `poetry build`_ to build a wheel for the local package,
    as specified via the ``distribution_format`` parameter. It returns a file
    URL with the absolute path to the built archive.

    The filename of the archive is extracted from the output Poetry writes
    to standard output, which currently looks like this::

        Building foobar (0.1.0)
        - Building wheel
        - Built foobar-0.1.0-py3-none-any.whl

    This is brittle, but it has the advantage that it does not rely on
    assumptions such as having a clean ``dist`` directory, or
    reconstructing the filename from the package metadata. (Poetry does not
    use PEP 440 for version numbers, so this is non-trivial.)

    .. _poetry build: https://python-poetry.org/docs/cli/#export

    Returns:
        The file URL for the distribution package.

    Raises:
        CommandSkippedError: The command `poetry build` was not executed.
    """
    output = self.poetry.session.run_always(  # type: ignore[attr-defined]
        "poetry",
        "build",
        "--format=wheel",
        external=True,
        silent=True,
        stderr=None,
    )

    if output is None:
        raise nox_poetry.poetry.CommandSkippedError(
            "The command `poetry build` was not executed"
            " (a possible cause is specifying `--no-install`)"
        )

    assert isinstance(output, str)  # noqa: S101

    wheel = Path("dist") / output.split()[-1]
    url: str = wheel.resolve().as_uri()

    return url


def installroot(self: nox_poetry.sessions._PoetrySession) -> None:
    """Install the root package into a Nox session using Poetry.

    This function installs the package located in the current directory into the
    session's virtual environment.
    """
    try:
        package = build_package(self)
    except nox_poetry.poetry.CommandSkippedError:
        pass
    else:
        self.session.install(package)  # type: ignore[attr-defined]


def install(session: nox.Session, *, groups: Iterable[str], only: bool = False) -> None:
    """Install the dependency groups using Poetry.

    Args:
        session: The Session object.
        groups: The dependency groups to install.
        only: Do not install the default dependencies.
    """
    session.run_always(
        "poetry",
        "install",
        "--no-root",
        "--sync",
        "--{}={}".format("only" if only else "with", ",".join(groups)),
        external=True,
    )
    if not only:
        installroot(nox_poetry.Session(session).poetry)


def activate_virtualenv_in_precommit_hooks(session: nox.Session) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    Args:
        session: The Session object.
    """
    assert session.bin is not None  # noqa: S101

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    hookdir = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        text = hook.read_text()
        bindir = repr(session.bin)[1:-1]  # strip quotes
        if not (
            Path("A") == Path("a") and bindir.lower() in text.lower() or bindir in text
        ):
            continue

        lines = text.splitlines()
        if not (lines[0].startswith("#!") and "python" in lines[0].lower()):
            continue

        header = dedent(
            f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """
        )

        lines.insert(1, header)
        hook.write_text("\n".join(lines))


@nox.session(name="pre-commit", python="3.10")
def precommit(session: nox.Session) -> None:
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    install(session, groups=["pre-commit"], only=True)
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@nox.session(python="3.10")
def safety(session: nox.Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = nox_poetry.Session(session).poetry.export_requirements()
    install(session, groups=["safety"], only=True)
    session.run("safety", "check", "--full-report", f"--file={requirements}")


@nox.session(python=python_versions)
def mypy(session: nox.Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or ["src", "tests", "docs/conf.py"]
    install(session, groups=["mypy", "tests"])
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@nox.session(python=python_versions)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    install(session, groups=["coverage", "tests"])

    if session.python == "3.10":
        # Workaround an unidentified issue in Poetry 1.2.0a2.
        session.install("coverage[toml]==6.1.2")

    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@nox.session
def coverage(session: nox.Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]

    install(session, groups=["coverage"], only=True)

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@nox.session(python=python_versions)
def typeguard(session: nox.Session) -> None:
    """Runtime type checking using Typeguard."""
    install(session, groups=["typeguard", "tests"])
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


@nox.session(python=python_versions)
def xdoctest(session: nox.Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    install(session, groups=["xdoctest"])
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(name="docs-build", python="3.10")
def docs_build(session: nox.Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["docs", "docs/_build"]
    install(session, groups=["docs"])

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)


@nox.session(python="3.10")
def docs(session: nox.Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    install(session, groups=["docs"])

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)
