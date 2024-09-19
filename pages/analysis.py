import pandas as pd
import numpy as np
import scipy
from scipy.signal import butter, lfilter
import streamlit as st

import plotly.graph_objects as go

from src2.navigation import navigation

from kswutils.calculator import calc_fft
from kswutils.signalprocessing import Sliding1d

from kswutils_plotly.plotly_graph import PlotlyGraph
from kswutils_fileio.fileio import FileIO
from kswutils_signal.frequency_analysis import FrequencyAnalysis


def read_data(f, loc="DE"):
    # name = FileIO.get_name_without_extion(f)
    # name = FileIO.get_name_without_extion(f).split('_')[0]
    name = f.name.split('_')[0]
    # loc = DE, FE, BA
    try:
        datadict = scipy.io.loadmat(f)  # dict
        data = datadict[f'X{name}_{loc}_time'][:, 0]
    except:
        return False
    return data


def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


class Analysis:
    def __init__(self) -> None:

        self.file = self.upload_file()

    def upload_file(self):
        container = st.container(height=None, border=True)

        with container:
            file = st.file_uploader(
                label="Upload a File", label_visibility="visible")

        return file

    def display(self):

        if self.file is not None:

            data = read_data(self.file)
            data = data[:12000*1]

            _x = np.linspace(0, len(data), len(data)) / 12000
            fig = PlotlyGraph.line(
                _x, data, title='Raw data in 1 Sec', ylabel="Acceleration [g]", xlabel="Time [Sec]")

            rpm = 29.95
            fm = 5.4152

            y = butter_bandpass_filter(data, 10, 300, 12000, 3)
            fft_x, fft_y = FrequencyAnalysis.calc_fft(y, 12000)
            fig2 = PlotlyGraph.line(
                fft_x, fft_y, xlim=[0, 300], title="FFT", label=["FFT"])

            class BBox:
                def __init__(self) -> None:
                    self.w = 2.5
                    self.h = 100

                    # Starting point, bottom-left point of the box
                    self.x = rpm * fm - 1.5

            bb = BBox()

            fig2.add_trace(
                go.Scatter(
                    x=[bb.x, bb.x, bb.x+bb.w, bb.x+bb.w, bb.x],
                    y=[0, bb.h, bb.h, 0, 0],
                    fill="toself",
                    mode="none",
                    name="Bounding Box",
                )
            )

            _text = f"<p style='font-family: Arial; color: red; font-size: 25px;'>Defect in Inner-race spotted.</p>"
            st.markdown(_text, unsafe_allow_html=True)

            container = st.container(height=None, border=True)
            with container:
                col1, col2 = st.columns(
                    [6, 6], vertical_alignment="top")

                with col1:
                    st.plotly_chart(fig)

                with col2:
                    st.plotly_chart(fig2)

            # df = pd.read_csv(self.file)

            # X = df["Acceleration"].to_numpy()

            # data = Sliding1d(X, window=2560, step=2560)
            # data_rms = data.rms_sliding()

            # fft_x, fft_y = calc_fft(X, 25600)
            # dff = {"x": fft_x, "y": fft_y}
            # dff = pd.DataFrame(dff)

            # container = st.container(height=None, border=True)
            # with container:

            #     col1, col2 = st.columns(
            #         [6, 6], vertical_alignment="top", gap="medium")

            # with col1:
            #     st.subheader("FFT")
            #     st.line_chart(dff.head(10000), x="x", y="y")

            # with col2:
            #     st.subheader("RMS")
            #     # st.line_chart(data=data_rms, x_label="Windows", y_label="RMS")

            #     _x = list(range(len(data_rms)))
            #     fig = PlotlyGraph.line(_x, data_rms, title="RMS")
            #     st.plotly_chart(fig)

        return None


navigation()

analysis = Analysis()
analysis.display()
