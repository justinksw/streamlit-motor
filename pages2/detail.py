import datetime
from random import random

import numpy as np
import streamlit as st

from src.anlysis import Analysis
from src.calculation import integrate_to_velocity

from src2.vae import calculate_abnomaly_score

class Detail:
    def __init__(self) -> None:

        motor_name = st.session_state["selected_motor"]

        # class Motor --> index.py
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

            motor_data = self.selected_motor.get_data()

            if not motor_data["Data"]:
                st.header("No data")

            else:
                idx = motor_data["Sensor Loc"].index(sensor_loc)
                y = motor_data["Data"][idx]

                ai_score = calculate_abnomaly_score(y)

                fs = int(st.session_state["sensor_fs"])

                x = np.linspace(0, len(y), len(y)) / fs
                label = motor_name

                vel = integrate_to_velocity(y, fs)
                rms = round(np.sqrt(np.mean(np.power(vel, 2))), 2)

                day = motor_data["Inspection Date"][idx]
                daydiff = datetime.datetime.today() - day

                motor_condition = "Warn"

                analysis.write_metrics(
                    motor_name, sensor_loc, motor_condition, daydiff.days, rms
                )

                analysis.gauge_indicator(ai_score, rms)

                analysis.plot_charts([x], [y], [label], fs)

        return True


def cancel_selection():
    st.session_state.selected_motor = None
    return None
