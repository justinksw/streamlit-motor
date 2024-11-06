import os
import json
import pytz
from datetime import datetime

import numpy as np
import pandas as pd

from kswutils_fileio.fileio import FileIO


class MotorJsonFileLocal:
    def __init__(self, file) -> None:

        self.file = file

        self.data_json = json.load(open(self.file))

    def get_file_name(self):
        # file name is unix timestamp, it is counting seconds
        return os.path.basename(self.file).split(".")[0]

    def get_timestamp_unix(self):
        name = self.get_file_name()

        ts = datetime.fromtimestamp(int(int(name.split(".")[0]) / 1000))
        # .replace(tzinfo=pytz.utc)
        return ts

    def get_timestamp_utc_hk(self):
        ts = self.get_timestamp_unix()

        ts_hk = ts.astimezone(pytz.timezone("Asia/Hong_Kong"))
        return ts_hk

    def get_device_id(self):
        return self.data_json["sensor_data"]["mac_address"]

    def get_battery_value(self):
        return self.data_json["battery_per"]

    def get_connection_value(self):
        return self.data_json["rssi"]

    def get_data_df(self):
        # json -> df
        data_df = pd.DataFrame(self.data_json["sensor_data"]["data"])
        # transpose
        data_df_T = data_df.T
        # add an index column
        data_df_T["index"] = list(range(len(data_df_T)))
        return data_df_T

    def get_data_array(self):
        # json -> df
        data_df = pd.DataFrame(self.data_json["sensor_data"]["data"])
        # transpose
        data_df_T = data_df.T

        return data_df_T.to_numpy()


class Motor:
    def __init__(self, motor_name: str, sensor_id_drive: str, sensor_id_non_drive: str):

        self.motor_name = motor_name  # e.g. "Motor 1"
        self.sensor_id_drive = sensor_id_drive  # e.g. "xxxx.cb"
        self.sensor_id_non_drive = sensor_id_non_drive  # e.g. "xxxx.0f"

    def get_latest_data(self, folder_dir, sensor=0):
        """
        sensor: 0 -> drive end sensor id

        sensor: 1 -> non-drive end sensor id
        """

        files = FileIO.get_subdirectories(folder_dir)
        files.sort(reverse=True)

        for f in files:
            _, file_extension = os.path.splitext(f)

            if file_extension != ".json":
                continue

            # print(file_extension)

            datafile = MotorJsonFileLocal(f)

            if datafile.get_device_id() == self.sensor_id_drive and sensor == 0:
                break
            elif datafile.get_device_id() == self.sensor_id_non_drive and sensor == 1:
                break

        data = datafile.get_data_array()
        battery = datafile.get_battery_value()

        # print(datafile.get_file_name())
        return data, battery

    def get_historical_data(self, folder_dir):

        files = FileIO.get_subdirectories(folder_dir)
        files.sort()

        historical_data = {
            "Filename": [],
            "RMS X": [],
            "RMS Y": [],
            "RMS Z": [],
            "TS HK": [],
            "Sensor ID": [],
            "Sensor Loc": [],
            "Battery": [],
        }

        for f in files:
            _, file_extension = os.path.splitext(f)

            if file_extension != ".json":
                continue

            datafile = MotorJsonFileLocal(f)

            data = datafile.get_data_array()

            # dc = np.repeat(np.array([[0, 0, 1]]), repeats=len(data), axis=0)
            # data_dc = data - dc
            rms = np.sqrt(np.mean(data**2, axis=0))

            historical_data["Filename"].append(datafile.get_file_name())
            historical_data["RMS X"].append(rms[0])
            historical_data["RMS Y"].append(rms[1])
            historical_data["RMS Z"].append(rms[2])
            historical_data["TS HK"].append(datafile.get_timestamp_utc_hk())
            historical_data["Sensor ID"].append(datafile.get_device_id())

            if datafile.get_device_id() == self.sensor_id_drive:
                historical_data["Sensor Loc"].append("Drive-end")

            elif datafile.get_device_id() == self.sensor_id_non_drive:
                historical_data["Sensor Loc"].append("Non-drive-end")

            historical_data["Battery"].append(datafile.get_battery_value())

        return historical_data
