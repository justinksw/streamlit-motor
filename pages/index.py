import streamlit as st

from pages_live.detail import Detail
from pages_live.overview import Overview

from src2.navigation import navigation


navigation()

# == Session state variables == #

if "selected_motor" not in st.session_state:
    st.session_state.selected_motor = None

if "selected_sensor" not in st.session_state:
    st.session_state.selected_sensor = "Sensor-1"

if "more_calculation" not in st.session_state:
    st.session_state.more_calculation = False

# == Main == #

if not st.session_state.selected_motor:

    overview = Overview()
    overview.display()

if st.session_state.selected_motor:

    detail = Detail()
    detail.display()
