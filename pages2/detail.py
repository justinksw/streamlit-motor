import datetime
from random import random

import numpy as np
import streamlit as st

from src.anlysis import Analysis
from src.calculation import integrate_to_velocity
from kswutils_signal.frequency_analysis import FrequencyAnalysis as FA


class Detail:
    def __init__(self) -> None:

        motor_name = st.session_state["selected_motor"]

        # class Motor
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

                fs = 1600
                if motor_name not in ["Motor 4", "Motor 7", "Motor 8"]:
                    fs = 50000

                x = np.linspace(0, len(y), len(y)) / fs
                label = motor_name

                ai = random() * (400 - 300) + 300

                if st.session_state["data_type"] == "Acceleration":
                    rms = np.sqrt(np.mean(np.power(y, 2)))

                elif st.session_state["data_type"] == "Velocity":
                    vel = integrate_to_velocity(y, fs)
                    rms = np.sqrt(np.mean(np.power(vel, 2)))

                rms = round(random() * (1 - 0.2) + 0.2, 2)

                day = motor_data["Inspection Date"][idx]
                daydiff = datetime.datetime.today() - day

                analysis.write_metrics(
                    motor_name, sensor_loc, motor_condition, daydiff.days, rms
                )

                analysis.gauge_indicator(ai, rms)

                analysis.plot_charts([x], [y], [label], fs)

        return True


def cancel_selection():
    st.session_state.selected_motor = None
    return None


# freq_signal = np.fft.fft(y)
# freq_signal[0] = 0  # remove dc component
# removed_dc = np.fft.ifft(freq_signal)
# modified_signal = np.real(removed_dc)
# modified_signal_ = FA.lowpass_filter(modified_signal, 1000, fs, order=3)
# rms = (
#     np.sqrt(np.mean(np.power(modified_signal, 2)))
#     * 9.81
#     / (2 * np.pi * fs)
# )
# rms = round(rms, 3)
# print(rms)
