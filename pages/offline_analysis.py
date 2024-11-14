import numpy as np
import streamlit as st

from src2.navigation import navigation
from pages2.do_anlysis import Analysis
from model_motor.motor import MotorJsonFile


class OfflineAnalysis:
    def __init__(self) -> None:

        self.files = self.upload_file()

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

        fs = 1600

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

        do_analysis = Analysis()
        do_analysis.plot_charts(X, Y, labels)


navigation()

analysis = OfflineAnalysis()
analysis.display()
