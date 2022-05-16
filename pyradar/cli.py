"""Console script for pyradar."""
import sys
import click

from .pyradar import run

@click.command()
@click.option('--video-dir', default='/tmp/pyradar', type=click.Path(), show_default=True, )
@click.option('--db', default='/tmp/pyradar/pyradar.db', type=click.Path(), show_default=True, )
@click.option('--min-speed', default=30.0, type=click.FLOAT, show_default=True)
@click.option('--min-recording-seconds', default=5.0, type=click.FLOAT, show_default=True)
def main(video_dir, db_path, min_speed, min_recording_seconds):
    """Console script for pyradar."""
    run(video_dir=video_dir, db_path=db_path, min_speed=min_speed, min_recording_seconds=min_recording_seconds)
    # click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
