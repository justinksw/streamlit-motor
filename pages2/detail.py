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
            if st.button("Drive end"):
                st.session_state["selected_sensor"] = "Drive-end"

        with col3:
            if st.button("Non-drive end"):
                st.session_state["selected_sensor"] = "Non-drive-end"

        self.datetime_now = datetime.date.today()

    def display(self):

        if st.session_state["selected_motor"]:

            motor_name = self.selected_motor.get_motor_name()
            sensor_loc = st.session_state["selected_sensor"]
            motor_condition = self.selected_motor.get_condition()

            analysis = Analysis()

            analysis.write_metrics(motor_name, sensor_loc, motor_condition, "N/A")

            motor_data = self.selected_motor.get_latest_data()

            if not motor_data["Data"]:
                st.header("No data")

            else:

                fs = 1600
                if motor_name not in ["Motor 4", "Motor 7", "Motor 8"]:
                    fs = 50000

                ai = random() * (300 - 200) + 200
                rms = random() * (1.5 - 0.2) + 0.2

                analysis.gauge_indicator(ai, rms)

                idx = motor_data["Sensor Loc"].index(sensor_loc)
                y = motor_data["Data"][idx]

                x = np.linspace(0, len(y), len(y)) / fs
                label = motor_name

                analysis.plot_charts([x], [y], [label], fs)

        return True


def cancel_selection():
    st.session_state.selected_motor = None
    return None
