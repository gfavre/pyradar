"""Console script for pyradar."""
import sys
import click

from .pyradar import run

@click.command()
@click.option('--video-dir', default='~/Documents', type=click.Path(exists=True))
def main(video_dir):
    """Console script for pyradar."""
    run(video_dir)
    # click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
