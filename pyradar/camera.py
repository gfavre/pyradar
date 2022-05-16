from pathlib import Path
from time import time

try:
    from picamera import PiCamera
    camera = PiCamera()
except ModuleNotFoundError:
    from unittest import mock
    camera = mock.MagicMock()


def start_recording(directory):
    """
    start recording of video in dir_name.
    dir_name: path to directory where to save videos
    return: filepath
    """
    dirpath = Path(directory)
    filename = str(time) + ".h264"
    filepath = dirpath / filename
    with open(filepath, 'wb') as video_file:
        camera.start_recording(video_file)
    return filepath


def stop_recording():
    camera.stop_recording()