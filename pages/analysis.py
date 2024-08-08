import pandas as pd
import streamlit as st

from src2.navigation import navigation

from kswutils.calculator import calc_fft
from kswutils.signalprocessing import Sliding1d


class Analysis:
    def __init__(self) -> None:

        self.file = self.upload_file()

    def upload_file(self):
        container = st.container(height=None, border=True)

        with container:
            file = st.file_uploader(
                label="Upload a CSV / Excel File", label_visibility="visible")
            
        return file
    
    def display(self):

        if self.file is not None:
            df = pd.read_csv(self.file)
            
            X = df["Acceleration"].to_numpy()

            data = Sliding1d(X, window=2560, step=2560)
            data_rms = data.rms_sliding()

            fft_x, fft_y = calc_fft(X, 25600)
            dff = {"x": fft_x, "y": fft_y}
            dff = pd.DataFrame(dff)

            container = st.container(height=None, border=True)
            with container:

                col1, col2 = st.columns(
                    [6, 6], vertical_alignment="top", gap="medium")

            with col1:
                st.subheader("FFT")
                st.line_chart(dff.head(10000), x="x", y="y")

            with col2:
                st.subheader("RMS")
                st.line_chart(data=data_rms, x_label="Windows", y_label="RMS")

        return None


navigation()

analysis = Analysis()
analysis.display()
