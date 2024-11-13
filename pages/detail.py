import datetime

import pandas as pd
import streamlit as st

from src.components import Static

from src2.ai_model import AI_Model

from pages.do_anlysis import Analysis

from kswutils.calculator import calc_fft
from kswutils.signalprocessing import Sliding1d


STATIC = Static()


class Detail:
    def __init__(self) -> None:

        self.selected_motor_name = st.session_state.selected_motor
        self.motors = st.session_state.motors

        self.selected_motor = self.motors[self.selected_motor_name]

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

    def display(self):

        if st.session_state.selected_motor:

            analysis = Analysis()

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
