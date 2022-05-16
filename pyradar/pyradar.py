#!/usr/bin/env python3
import logging
from time import time

import serial

from .camera import start_recording, stop_recording
from .db import save_event, init_db


logger = logging.getLogger(__name__)

# Ops241A module settings:  kph, dir off, 20Ksps, min -9dB pwr, squelch 5000
OPS241A_SPEED_OUTPUT_UNITS = 'UK'
OPS241A_DIRECTION_CONTROL = 'Od'
Ops241A_Sampling_Frequency = 'S2'
Ops241A_Transmit_Power = 'PX'
Ops241A_Threshold_Control = 'QI'
Ops241A_Module_Information = '??'
Ops241A_Data_Accuracy = 'F1'

MIN_RECORDING_SECONDS = 5.0
MIN_SPEED = 10.0


class RadarSensor:
    def __init__(self):
        self._sensor = self._get_sensor(timeout=1)
        self._configure_sensor()
        self.set_timeout(0.01)

    def _configure_sensor(self):
        self.send_command(OPS241A_SPEED_OUTPUT_UNITS)
        self.send_command(OPS241A_DIRECTION_CONTROL)
        self.send_command(Ops241A_Sampling_Frequency)
        self.send_command(Ops241A_Transmit_Power)
        self.send_command(Ops241A_Threshold_Control)
        self.send_command(Ops241A_Data_Accuracy)
        self.send_command(Ops241A_Module_Information)

    def _get_sensor(self, timeout):
        sensor = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout,
            writeTimeout=2
        )
        sensor.flushInput()
        sensor.flushOutput()
        return sensor

    def set_timeout(self, timeout):
        self._sensor = self._get_sensor(timeout=timeout)

    def send_command(self, command):
        encoded_command = str.encode(command)
        self._sensor.write(encoded_command)
        ser_message_start = '{'
        ser_write_verify = False
        # Print out module response to command string
        while not ser_write_verify:
            data_rx_bytes = self._sensor.readline()
            data_rx_length = len(data_rx_bytes)
            if data_rx_length != 0:
                data_rx_str = str(data_rx_bytes)
                if data_rx_str.find(ser_message_start):
                    ser_write_verify = True

    def readline(self):
        return self._sensor.readline()

    def read_speed(self):
        rx_bytes = self.readline()
        if len(rx_bytes) and '{' not in str(rx_bytes):
            return abs(float(rx_bytes))


def run(video_dir, db_path, min_speed=MIN_SPEED, min_recording_seconds=MIN_RECORDING_SECONDS):
    logger.info(" [*] Waiting for events. To exit press CTRL+C")
    init_db(db_path)
    sensor = RadarSensor()
    recording = False
    max_recorded_speed = 0.0
    video_path = None
    start_time = time()
    while True:
        speed = sensor.read_speed()

        if speed is None:
            delta_time = time() - start_time
            if delta_time > min_recording_seconds:
                if recording:
                    # we were registering a speed break, let's store it
                    stop_recording()
                    recording = False
                    save_event(max_recorded_speed, video_path)
                    max_recorded_speed = 0
                    logger.info(f"end of event, max speed: {max_recorded_speed}")
            continue
        if not recording and speed > min_speed:
            logger.info("new event, start recording")
            video_path = start_recording(video_dir)
            recording = True
            max_recorded_speed = speed
            start_time = time()
        if float(speed) > max_recorded_speed:
            max_recorded_speed = speed
