import pandas as pd
import numpy as np
import scipy
from scipy.signal import butter, lfilter
import streamlit as st

import plotly.graph_objects as go

from src2.navigation import navigation
from src2.plots import Plots

from kswutils.calculator import calc_fft
from kswutils.signalprocessing import Sliding1d

from kswutils_plotly.plotly_graph import PlotlyGraph
from kswutils_fileio.fileio import FileIO
from kswutils_signal.frequency_analysis import FrequencyAnalysis


def read_data(f, loc="DE"):
    # name = FileIO.get_name_without_extion(f)
    # name = FileIO.get_name_without_extion(f).split('_')[0]
    name = f.name.split("_")[0]
    # loc = DE, FE, BA
    try:
        datadict = scipy.io.loadmat(f)  # dict
        data = datadict[f"X{name}_{loc}_time"][:, 0]
    except:
        return False
    return data


def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype="band")


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


class Analysis:
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

        # == Row 1 == #

        container = st.container(border=True)
        with container:
            col1, col2, col3 = st.columns(3)

            with col1:
                show_1 = st.checkbox("Show Raw Data and Statistic", True)
            with col2:
                show_2 = st.checkbox("Show Spectrum", True)
            with col3:
                show_3 = st.checkbox("Show Others", False)

        # == ROW 2 == #

        container = st.container(border=True)
        with container:

            st.subheader("Select a Time Window [Sec]")

            d = st.slider(
                "Slide to select a time window to inspect",
                min_value=0.0,
                max_value=5.0,
                value=(1.0, 1.5),
                step=0.05,
            )

        # == Plot Setting == #

        plot = Plots(
            files=self.files,
            selected_time_window=d,
        )

        # == ROW 3 == #

        if show_1:
            container = st.container(border=True)
            with container:
                st.subheader("Temporal Analysis")

                col1, col2 = st.columns(2, gap="medium")
                with col1:
                    st.plotly_chart(plot.plot_raw_data())

                with col2:
                    st.plotly_chart(plot.plot_statistic())

        # == ROW 4 == #

        ref = {
            "Show RPM": 0,
            "Show BPFI": 0,
            "Show BPFO": 0,
            "Show BSF": 0,
            "Show FTF": 0,
            "RPM": 0,
            "BPFI": 0,
            "BPFO": 0,
            "BSF": 0,
            "FTF": 0,
        }

        container = st.container(border=True)
        with container:

            st.subheader("Visualize characteristic frequencies")

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                ref["RPM"] = int(st.text_input("Rotation Speed (RPM)", "1840")) / 60
                ref["Show RPM"] = st.checkbox("Show RPM")

            with col2:
                ref["BPFI"] = (
                    float(st.text_input("BPFI (Inner Race)", "5.0020")) * ref["RPM"]
                )
                ref["Show BPFI"] = st.checkbox("Show BPFI")

            with col3:
                ref["BPFO"] = (
                    float(st.text_input("BPFO (Outer Race)", "2.9980")) * ref["RPM"]
                )
                ref["Show BPFO"] = st.checkbox("Show BPFO")

            with col4:
                ref["BSF"] = (
                    float(st.text_input("BSF (Ball Spin)", "1.8710")) * ref["RPM"]
                )
                ref["Show BSF"] = st.checkbox("Show BSF")

            with col5:
                ref["FTF"] = float(st.text_input("FTF (Cage)", "0.3750")) * ref["RPM"]
                ref["Show FTF"] = st.checkbox("Show FTF")

        # == ROW 5 == #

        if show_2:
            container = st.container(border=True)
            with container:

                st.subheader("Spectral Analysis")

                col1, col2 = st.columns(2, gap="medium")
                with col1:
                    st.plotly_chart(plot.plot_fft(ref))
                with col2:
                    st.plotly_chart(plot.plot_envelope_fft(ref))

        # == ROW 6 == #

        if show_3:
            container = st.container(border=True)
            with container:

                col1, col2 = st.columns(2, gap="medium")
                with col1:
                    st.plotly_chart(plot.plot_envelope_fft_with_filter(ref))
                    st.plotly_chart(plot.plot_envelope_fft_with_denoising_filter(ref))
                with col2:
                    st.plotly_chart(plot.plot_envelope_fft_with_wavelet_denosing(ref))

        return None


navigation()

analysis = Analysis()
analysis.display()
