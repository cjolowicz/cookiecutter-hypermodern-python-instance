"""Command-line interface."""
import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    """Cookiecutter Hypermodern Python Instance."""


def this_function_has_no_coverage(n: int) -> int:
    """This function has no coverage."""
    return n + 1
