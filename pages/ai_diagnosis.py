import streamlit as st

from src2.vae import diagnose
from src2.navigation import navigation


navigation()

def block(name):
    container = st.container(height=None, border=True)
    with container:
        col1, col2 = st.columns([6, 6], vertical_alignment="center", gap="medium")

        with col1:
            st.title(name)

        with col2:
            motor_data = st.session_state["motors"][name].get_data()
            y = motor_data["Data"][0]
            predict = diagnose(y)
            st.title(predict)


block("Motor 1")
block("Motor 2")
block("Motor 3")
block("Motor 4")
block("Motor 5")
block("Motor 6")
