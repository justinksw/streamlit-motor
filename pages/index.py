import streamlit as st

from pages2.detail import Detail
from pages2.overview import Overview

from src.motor import Motor

from src2.navigation import navigation


navigation()

# == Session state variables == #

# == Motors configurations == #

if "motors" not in st.session_state:

    st.session_state["motors"] = {
        "Motor 1": Motor(
            motor_name="Motor 1",
            sensor_id_drive="NA",
            sensor_id_non_drive="NA",
            datafolder="NA",
        ),
        "Motor 2": Motor(
            motor_name="Motor 2",
            sensor_id_drive="NA",
            sensor_id_non_drive="NA",
            datafolder="NA",
        ),
        "Motor 3": Motor(
            motor_name="Motor 3",
            sensor_id_drive="NA",
            sensor_id_non_drive="NA",
            datafolder="NA",
        ),
        "Motor 4": Motor(
            motor_name="Motor 4",
            sensor_id_drive="00:13:a2:00:42:35:db:cb",
            sensor_id_non_drive="00:13:a2:00:42:30:83:0f",
            datafolder="data/CLP20241024data/Motor 4",
        ),
        "Motor 5": Motor(
            motor_name="Motor 5",
            sensor_id_drive="NA",
            sensor_id_non_drive="NA",
            datafolder="NA",
        ),
        "Motor 6": Motor(
            motor_name="Motor 6",
            sensor_id_drive="NA",
            sensor_id_non_drive="NA",
            datafolder="NA",
        ),
        "Motor 7": Motor(
            motor_name="Motor 7",
            sensor_id_drive="00:13:a2:00:42:35:db:cb",
            sensor_id_non_drive="00:13:a2:00:42:30:83:0f",
            datafolder="data/CLP20241024data/Motor 4",
        ),
        "Motor 8": Motor(
            motor_name="Motor 8",
            sensor_id_drive="00:13:a2:00:42:35:db:cb",
            sensor_id_non_drive="00:13:a2:00:42:30:83:0f",
            datafolder="data/CLP20241024data/Motor 4",
        ),
    }


# == Other global session state variables == #

if "selected_motor" not in st.session_state:
    st.session_state["selected_motor"] = None

if "selected_sensor" not in st.session_state:
    st.session_state["selected_sensor"] = "Drive-end"


# == Main == #

if not st.session_state["selected_motor"]:

    overview = Overview()
    overview.display()

if st.session_state["selected_motor"]:

    detail = Detail()
    detail.display()
