"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Cookiecutter Hypermodern Python Instance."""


if __name__ == "__main__":
    main(prog_name="cookiecutter-hypermodern-python-instance")  # pragma: no cover
