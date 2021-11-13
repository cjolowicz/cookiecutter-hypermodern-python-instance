"""Nox sessions."""
import hashlib
import shutil
import sys
from pathlib import Path
from textwrap import dedent
from typing import Iterable
from typing import Iterator

import nox

try:
    import nox_poetry.poetry
    import nox_poetry.sessions
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


def install(session: nox.Session, *, groups: Iterable[str], root: bool = True) -> None:
    """Install the dependency groups using Poetry.

    This function installs the given dependency groups into the session's
    virtual environment. When ``root`` is true (the default), the function
    also installs the root package and its default dependencies.

    To avoid an editable install, the root package is not installed using
    ``poetry install``. Instead, the function uses ``poetry build`` to build a
    wheel for the root package, and installs the wheel using ``pip install``.

    The filename of the archive is extracted from the output Poetry writes
    to standard output, which currently looks like this::

        Building foobar (0.1.0)
        - Building wheel
        - Built foobar-0.1.0-py3-none-any.whl

    This is brittle, but it has the advantage that it does not rely on
    assumptions such as having a clean ``dist`` directory, or
    reconstructing the filename from the package metadata. (Poetry does not
    use PEP 440 for version numbers, so this is non-trivial.)

    Args:
        session: The Session object.
        groups: The dependency groups to install.
        root: Install the root package.
    """
    session.run_always(
        "poetry",
        "install",
        "--no-root",
        "--sync",
        "--{}={}".format("only" if not root else "with", ",".join(groups)),
        external=True,
    )
    if not root:
        return

    output = session.run_always(
        "poetry", "build", "--format=wheel", external=True, silent=True, stderr=None
    )

    if output is None:
        # The package build was skipped due to `--no-install`.
        return

    assert isinstance(output, str)  # noqa: S101

    wheel = Path("dist") / output.split()[-1]
    session.install(wheel.resolve().as_uri())


def export(self: nox_poetry.poetry.Poetry) -> str:
    """Export the lock file to requirements format.

    Returns:
        The generated requirements as text.

    Raises:
        CommandSkippedError: The command `poetry export` was not executed.
    """
    output = self.session.run_always(
        "poetry",
        "export",
        "--format=requirements.txt",
        "--dev",
        *[f"--extras={extra}" for extra in self.config.extras],
        "--without-hashes",
        external=True,
        silent=True,
        stderr=None,
    )

    if output is None:
        raise nox_poetry.poetry.CommandSkippedError(
            "The command `poetry export` was not executed"
            " (a possible cause is specifying `--no-install`)"
        )

    assert isinstance(output, str)  # noqa: S101

    def _stripwarnings(lines: Iterable[str]) -> Iterator[str]:
        for line in lines:
            if line.startswith("Warning:"):
                print(line, file=sys.stderr)
                continue
            yield line

    return "".join(_stripwarnings(output.splitlines(keepends=True)))


def export_requirements(self: nox_poetry.sessions._PoetrySession) -> Path:
    """Export a requirements file from Poetry.

    This function uses `poetry export`_ to generate a :ref:`requirements
    file <Requirements Files>` containing the project dependencies at the
    versions specified in ``poetry.lock``. The requirements file includes
    both core and development dependencies.

    The requirements file is stored in a per-session temporary directory,
    together with a hash digest over ``poetry.lock`` to avoid generating the
    file when the dependencies have not changed since the last run.

    .. _poetry export: https://python-poetry.org/docs/cli/#export

    Returns:
        The path to the requirements file.
    """
    # Avoid ``session.virtualenv.location`` because PassthroughEnv does not
    # have it. We'll just create a fake virtualenv directory in this case.

    tmpdir = Path(self.session._runner.envdir) / "tmp"  # type: ignore[attr-defined]
    tmpdir.mkdir(exist_ok=True, parents=True)

    path = tmpdir / "requirements.txt"
    hashfile = tmpdir / f"{path.name}.hash"

    lockdata = Path("poetry.lock").read_bytes()
    digest = hashlib.blake2b(lockdata).hexdigest()

    if not hashfile.is_file() or hashfile.read_text() != digest:
        path.write_text(self.poetry.export())  # type: ignore[attr-defined]
        hashfile.write_text(digest)

    return path


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
    install(session, groups=["pre-commit"], root=False)
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@nox.session(python="3.10")
def safety(session: nox.Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = export_requirements(nox_poetry.Session(session).poetry)
    install(session, groups=["safety"], root=False)
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

    install(session, groups=["coverage"], root=False)

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
