import datetime
from random import random

import numpy as np
import streamlit as st

from src.anlysis import Analysis


class Detail:
    def __init__(self) -> None:

        motor_name = st.session_state["selected_motor"]

        self.selected_motor = st.session_state["motors"][motor_name]

        st.write(datetime.date.today())

        col1, col2, col3 = st.columns(3)

        with col1:
            st.button("Return", on_click=cancel_selection)

        with col2:
            if st.button("Sensor 1"):
                st.session_state["selected_sensor"] = "Sensor-1"

        with col3:
            if st.button("Sensor 2"):
                st.session_state["selected_sensor"] = "Sensor-2"

        self.datetime_now = datetime.date.today()

    def display(self):

        if st.session_state["selected_motor"]:

            motor_name = self.selected_motor.get_motor_name()
            sensor_id = st.session_state["selected_sensor"]
            motor_condition = self.selected_motor.get_condition()

            analysis = Analysis()

            analysis.write_metrics(motor_name, sensor_id, motor_condition, "N/A")

            ai = random() * (500 - 100) + 100
            rms = random() * (1.5 - 0.2) + 0.2

            analysis.gauge_indicator(ai, rms)

            motor_data = self.selected_motor.get_latest_data()

            # print(motor_data["Data"][0].shape)

            y = motor_data["Data"][0]
            x = np.linspace(0, len(y), len(y)) / 1600
            label = motor_name

            analysis.plot_charts([x], [y], [label])

        return True


def cancel_selection():
    st.session_state.selected_motor = None
    return None
