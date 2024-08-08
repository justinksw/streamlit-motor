import datetime

import pandas as pd
import streamlit as st

from src.components import Static
from src.database import Database
from src2.ai_model import AI_Model

from kswutils.calculator import calc_fft
from kswutils.signalprocessing import Sliding1d


STATIC = Static()
DATABASE = Database()


class Detail:
    def __init__(self) -> None:
        self.motor = st.session_state.selected_motor

        st.write(datetime.date.today())

        col1, col2, col3 = st.columns(3)

        with col1:
            st.button("Return", on_click=cancel_selection)

        with col2:
            if st.button("Sensor 1"):
                st.session_state.selected_sensor = "Sensor-1"

        with col3:
            if st.button("Sensor 2"):
                st.session_state.selected_sensor = "Sensor-2"

        self.datetime_now = datetime.date.today()

    def text_metrics(self):

        if self.motor == "Motor 1":
            value = "Good"
            last_inspection_date = datetime.date(2023, 10, 20)
        elif self.motor == "Motor 2":
            value = "Damaged"
            last_inspection_date = datetime.date(2023, 10, 26)
        elif self.motor == 'Motor 3':
            value = "Damaged"
            last_inspection_date = datetime.date(2023, 11, 4)
        elif self.motor == "Motor 4":
            value = "Damaged"
            last_inspection_date = datetime.date(2023, 11, 1)
        elif self.motor == "Motor 5":
            value = "Danger"
            last_inspection_date = datetime.date(2024, 1, 18)
        diff = abs(self.datetime_now - last_inspection_date).days

        container = st.container(height=None, border=True)
        with container:

            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label="Motor", value=f"{self.motor}")
            col2.metric(label="Sensor",
                        value=f"{st.session_state.selected_sensor}")
            col3.metric(label="Condition", value=value)
            col4.metric(
                label="Since last inspection", value=f"{diff} day(s)")
        return None

    def gauge_indicator(self):

        st.header("Health Indicator")

        condition = ""

        if self.motor == "Motor 1":
            condition = "lub100"
            m2 = 0.8
        elif self.motor == "Motor 2":
            condition = "lub75"
            m2 = 2.2
        elif self.motor == 'Motor 3':
            condition = "lub25"
            m2 = 4.5
        elif self.motor == "Motor 4":
            condition = "lub10"
            m2 = 5.5
        elif self.motor == "Motor 5":
            condition = "lub2_5"
            m2 = 12

        else:
            m2 = 0

        if condition:

            df = DATABASE.get_data(condition)

            X = df["data"].to_numpy()

            AI = AI_Model(
                encoder_pt='./model/encoder1.pt',
                deconde_pt='./model/decoder1.pt',)

            feature = AI.get_feature(X)

            score = AI.anomaly_detection(
                data=feature
            )

        container = st.container(height=None, border=True)
        with container:

            col1, col2 = st.columns(
                [6, 6], vertical_alignment="top", gap="medium")

            with col1:
                STATIC.gauge_chart_ai(value=score)

            with col2:
                STATIC.gauge_chart_rms(value=m2)

        return None

    def write_df(self):

        st.header("Motor Data")

        condition = ""

        if self.motor == "Motor 1":
            condition = "lub100"
        elif self.motor == "Motor 2":
            condition = "lub75"
        elif self.motor == 'Motor 3':
            condition = "lub25"
        elif self.motor == "Motor 4":
            condition = "lub10"
        elif self.motor == "Motor 5":
            condition = "lub2_5"

        if condition:
            df = DATABASE.get_data(condition)

            X = df["data"].to_numpy()

            data = Sliding1d(X, window=2560, step=256)
            data_rms = data.rms_sliding()

            fft_x, fft_y = calc_fft(X, 25600)
            dff = {"Frequency (Hz)": fft_x, "Coefficient": fft_y}
            dff = pd.DataFrame(dff)

            container = st.container(height=None, border=True)
            with container:

                col1, col2 = st.columns(
                    [6, 6], vertical_alignment="top", gap="medium")

                if not st.session_state.more_calculation:
                    st.button("More", on_click=show_more_calculation)

                else:
                    st.button("Less", on_click=hide_more_calculation)

            with col1:
                st.subheader("RMS")
                st.line_chart(data=data_rms, x_label="Windows", y_label="RMS")

                if st.session_state.more_calculation:
                    st.subheader("Skew")
                    st.line_chart(data=data.skew_sliding(),
                                  x_label="Windows", y_label="Skew")

            with col2:
                st.subheader("FFT")
                st.line_chart(dff.head(500), x="Frequency (Hz)",
                              y="Coefficient")

                if st.session_state.more_calculation:
                    st.subheader("Kurtosis")
                    st.line_chart(data=data.kurtosis_sliding(),
                                  x_label="Windows", y_label="Kurtosis",)

        return None

    def display(self):

        if self.motor:

            self.text_metrics()
            self.gauge_indicator()
            self.write_df()

        return True


def cancel_selection():
    st.session_state.selected_motor = None
    return None


def show_more_calculation():
    if st.session_state.more_calculation == False:
        st.session_state.more_calculation = True
    return None


def hide_more_calculation():
    if st.session_state.more_calculation == True:
        st.session_state.more_calculation = False
    return None
