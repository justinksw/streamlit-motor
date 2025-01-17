import numpy as np
import streamlit as st

from src.anlysis import Analysis
from src.motor import MotorJsonFile

from src2.navigation import navigation


class OfflineAnalysis:
    def __init__(self) -> None:

        self.files = self.upload_file()

        # col1, col2 = st.columns(2, vertical_alignment="center")
        # with col1:
        #     self.fs = st.text_input("Sensor Sampling Rate (Hz)", "1600")
        # with col2:
        #     st.text_input("Motor Rotation Speed (RPM)", "1488")

    def upload_file(self):
        container = st.container(height=None, border=True)

        with container:
            files = st.file_uploader(
                label="Upload File(s)",
                label_visibility="visible",
                accept_multiple_files=True,
            )
        return files

    def display(self):

        if not self.files:
            return None

        # Local analysis: files: directories
        # Online analysis: files: streamlit upload file objects

        fs = int(st.session_state["sensor_fs"])

        datafiles = [MotorJsonFile(i, local=False) for i in self.files]

        Y = []
        X = []
        labels = []

        for m in datafiles:

            _y = m.get_data()
            _x = np.linspace(0, len(_y), len(_y)) / fs

            Y.append(_y)
            X.append(_x)
            labels.append(m.get_file_name())

        analysis = Analysis()
        analysis.plot_charts(X, Y, labels, fs)


navigation()

offline_analysis = OfflineAnalysis()
offline_analysis.display()
