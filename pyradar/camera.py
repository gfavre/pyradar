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
    dirpath.mkdir(exist_ok=True)
    filename = str(time()) + ".h264"
    filepath = dirpath / filename
    camera.start_recording(str(filepath))
    return filepath


def stop_recording():
    camera.stop_recording()
