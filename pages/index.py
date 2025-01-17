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
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/test/Motor_1",
        ),
        "Motor 2": Motor(
            motor_name="Motor 2",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/test/Motor_2",
        ),
        "Motor 3": Motor(
            motor_name="Motor 3",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/test/Motor_3",
        ),
        "Motor 4": Motor(
            motor_name="Motor 4",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/test/Motor_4",
        ),
        "Motor 5": Motor(
            motor_name="Motor 5",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/test/Motor_5",
        ),
        "Motor 6": Motor(
            motor_name="Motor 6",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/test/Motor_6",
        ),
        "Motor 7": Motor(
            motor_name="Motor 7",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/test/Motor_7",
        ),
        "Motor 8": Motor(
            motor_name="Motor 8",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/test/Motor_8",
        ),
    }


# == Other global session state variables == #

if "data_type" not in st.session_state:
    st.session_state["data_type"] = "Acceleration"

if "selected_motor" not in st.session_state:
    st.session_state["selected_motor"] = None

if "selected_sensor" not in st.session_state:
    st.session_state["selected_sensor"] = "Drive-end"

if "motor_rpm" not in st.session_state:
    st.session_state["motor_rpm"] = 1740

if "sensor_fs" not in st.session_state:
    st.session_state["sensor_fs"] = 50000

# == Main == #

if not st.session_state["selected_motor"]:

    overview = Overview()
    overview.display()

if st.session_state["selected_motor"]:

    detail = Detail()
    detail.display()
