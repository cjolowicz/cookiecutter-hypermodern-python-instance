"""Command-line interface."""
import sys

import click


@click.command()
@click.version_option()
def main() -> None:
    """Cookiecutter Hypermodern Python Instance."""
    if sys.version_info >= (3, 8):
        click.echo("Python 3.8+")
    elif sys.version_info >= (3, 7):
        click.echo("Python 3.7")
    else:
        click.echo("Python 3.6 or less")


if __name__ == "__main__":
    main(prog_name="cookiecutter-hypermodern-python-instance")  # pragma: no cover
