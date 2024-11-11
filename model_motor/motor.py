import os
import json
import pytz
from datetime import datetime

import numpy as np
import pandas as pd

from kswutils_fileio.fileio import FileIO


class MotorJsonFile:
    def __init__(self, file, local=False) -> None:

        if local:
            self.name = os.path.basename(file)
            self.data_json = json.load(open(file))

        else:  # Streamlit file uploader
            self.name = file.name
            self.data_json = json.loads(file.getvalue())

    def get_file_name(self):
        # file name is unix timestamp, it is counting seconds
        return self.name.split(".")[0]

    def get_timestamp_unix(self):

        ts = datetime.fromtimestamp(int(int(self.name.split(".")[0]) / 1000))
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

    def get_data(self):
        # json -> df
        data_df = pd.DataFrame(self.data_json["sensor_data"]["data"])
        # transpose
        data_df_T = data_df.T

        data_array = data_df_T.to_numpy()

        return data_array[:, 2]


class Motor:

    def __init__(
        self,
        motor_name: str,
        sensor_id_drive: str,
        sensor_id_non_drive: str,
        datafolder: str,
    ):

        self.motor_name = motor_name  # e.g. "Motor 1"
        self.sensor_id_drive = sensor_id_drive  # e.g. "xxxx.cb"
        self.sensor_id_non_drive = sensor_id_non_drive  # e.g. "xxxx.0f"
        self.datafolder = datafolder

        self.motor_data_latest = self.get_latest_data()

    def get_latest_data(self):

        motor_data = {
            "Motor Name": [],
            "Data": [],
            "Sensor ID": [],
            "Sensor Loc": [],
            "Battery": [],
        }

        flag1 = False
        flag2 = False

        if os.path.exists(self.datafolder):

            files = FileIO.get_subdirectories(self.datafolder)
            files.sort(reverse=True)

            for f in files:
                _, file_extension = os.path.splitext(f)
                if file_extension != ".json":
                    continue
                datafile = MotorJsonFile(f, local=True)

                if not flag1 and datafile.get_device_id() == self.sensor_id_drive:

                    motor_data["Motor Name"].append(self.motor_name)
                    motor_data["Data"].append(datafile.get_data_array())
                    motor_data["Sensor ID"].append(datafile.get_device_id())
                    motor_data["Sensor Loc"].append("Drive-end")

                    flag1 = True

                if not flag2 and datafile.get_device_id() == self.sensor_id_non_drive:

                    motor_data["Motor Name"].append(self.motor_name)
                    motor_data["Data"].append(datafile.get_data_array())
                    motor_data["Sensor ID"].append(datafile.get_device_id())
                    motor_data["Sensor Loc"].append("Non-drive-end")

                    flag2 = True

                if flag1 and flag2:
                    break

        if not flag1 or not flag2:
            return {
                "Motor Name": [self.motor_name],
                "Data": [],
                "Sensor ID": [],
                "Sensor Loc": [],
                "Battery": [],
            }

        return motor_data

    def get_motor_name(self):
        return self.motor_name

    def get_condition(self):

        if not self.motor_data_latest["Data"]:
            return "N/A"

        # calculate the rms, compare to standard

        return "Health"

    def get_battery(self):

        if not self.motor_data_latest["Data"]:
            return (0, 0)

        return ("100", "100")

    def get_last_inspection_date(self):

        if not self.motor_data_latest["Data"]:
            return "N/A"

        return "2024/10/24"


def get_historical_data(folder_dir):

    files = FileIO.get_subdirectories(folder_dir)
    files.sort()

    historical_data = {
        "File Name": [],
        "RMS X": [],
        "RMS Y": [],
        "RMS Z": [],
        "TS HK": [],
        "Sensor ID": [],
        # "Sensor Loc": [],
        "Battery": [],
    }

    for f in files:
        _, file_extension = os.path.splitext(f)

        if file_extension != ".json":
            continue

        datafile = MotorJsonFile(f, local=True)

        data = datafile.get_data_array()

        # dc = np.repeat(np.array([[0, 0, 1]]), repeats=len(data), axis=0)
        # data_dc = data - dc
        rms = np.sqrt(np.mean(data**2, axis=0))

        historical_data["File Name"].append(datafile.get_file_name())
        historical_data["RMS X"].append(rms[0])
        historical_data["RMS Y"].append(rms[1])
        historical_data["RMS Z"].append(rms[2])
        historical_data["TS HK"].append(datafile.get_timestamp_utc_hk())
        historical_data["Sensor ID"].append(datafile.get_device_id())

        # if datafile.get_device_id() == self.sensor_id_drive:
        #     historical_data["Sensor Loc"].append("Drive-end")

        # elif datafile.get_device_id() == self.sensor_id_non_drive:
        #     historical_data["Sensor Loc"].append("Non-drive-end")

        historical_data["Battery"].append(datafile.get_battery_value())

    return historical_data
