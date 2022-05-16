"""Console script for pyradar."""
import sys
import click

from .pyradar import run

@click.command()
def main(args=None):
    """Console script for pyradar."""
    run()
    # click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
