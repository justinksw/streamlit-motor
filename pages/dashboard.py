import datetime

import numpy as np
import pandas as pd
import streamlit as st

from src.navigation import navigation
from src.guage import gauge
from src.use_vae import get_feature, anomaly_detection

from kswutils.calculator import calc_fft
from kswutils.signalprocessing import Sliding1d


class Motor:
    # input: Query.
    # -> dataframe
    # return current status of the motor

    def __init__(self, conn, motor) -> None:

        query = f"SELECT data, label FROM lub WHERE label='{motor}';"

        table = conn.query(query, ttl=0)
        df = pd.DataFrame(table)

        pass


class Dashboard:
    def __init__(self) -> None:

        self.conn = st.connection('mysql', type='sql')

        

        self.datetime_now = datetime.date.today()
        st.write(self.datetime_now)

        self.motor = self.select_box()

    def select_box(self):

        container = st.container(height=None, border=True)
        with container:

            motor_selection = st.selectbox(
                label="Select a motor for inspection.",
                options=[
                    "Motor 1",  # 100%
                    "Motor 2",  # 75%
                    "Motor 3",  # 25%
                    "Motor 4",  # 10%
                    "Motor 5",  # 2.5%
                ],
                index=None,
            )
        return motor_selection

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

            col1, col2, col3 = st.columns(3)
            col1.metric(label="Motor", value=f"{self.motor}")
            col2.metric(label="Condition", value=value)
            col3.metric(
                label="Since last inspection", value=f"{diff} day(s)")
        return None

    def gauge_indicator(self):

        st.header("Health Condition Indicator - VAE")

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
            query = f"SELECT data, label FROM lub WHERE label='{condition}';"

            table = self.conn.query(query, ttl=0)
            df = pd.DataFrame(table)

            # st.dataframe(df)

            X = df["data"].to_numpy()

            feature = get_feature(X)

            score = anomaly_detection(
                data=feature,
                encoder_pt='./model/encoder1.pt',
                deconde_pt='./model/decoder1.pt',
            )
            print(score)
            print()

        container = st.container(height=None, border=True)
        with container:

            col1, col2 = st.columns(
                [6, 6], vertical_alignment="top", gap="medium")

            with col1:
                fig1 = gauge(value=int(score), title="Indicator 1")
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                fig2 = gauge(value=int(score), title="Indicator 2")
                st.plotly_chart(fig2, use_container_width=True)

        return None

    def write_df(self):

        st.header("Connected Local MySQL database")

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
            query = f"SELECT data, label FROM lub WHERE label='{condition}';"

            table = self.conn.query(query, ttl=0)
            df = pd.DataFrame(table)

            # st.dataframe(df)

            X = df["data"].to_numpy()

            data = Sliding1d(X, window=2560, step=256)
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
                st.line_chart(dff.head(500), x="x", y="y")

            with col2:
                st.subheader("RMS")
                st.line_chart(data=data_rms, x_label="Windows", y_label="RMS")

        return None

    def display(self):

        if self.motor:

            self.text_metrics()
            self.gauge_indicator()

            self.write_df()

        return True


navigation()

dashboard = Dashboard()
dashboard.display()
