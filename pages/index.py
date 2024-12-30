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
            datafolder="data/CLP20241024data/Motor 1 (dummy)",
        ),
        "Motor 2": Motor(
            motor_name="Motor 2",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/CLP20241024data/Motor 2 (dummy)",
        ),
        "Motor 3": Motor(
            motor_name="Motor 3",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/CLP20241024data/Motor 3 (dummy)",
        ),
        "Motor 4": Motor(
            motor_name="Motor 4",
            sensor_id_drive="00:13:a2:00:42:35:db:cb",
            sensor_id_non_drive="00:13:a2:00:42:30:83:0f",
            datafolder="data/CLP20241024data/Motor 4",
        ),
        "Motor 5": Motor(
            motor_name="Motor 5",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/CLP20241024data/Motor 5 (dummy)",
        ),
        "Motor 6": Motor(
            motor_name="Motor 6",
            sensor_id_drive="drive",
            sensor_id_non_drive="non-drive",
            datafolder="data/CLP20241024data/Motor 6 (dummy)",
        ),
        "Motor 7": Motor(
            motor_name="Motor 7",
            sensor_id_drive="00:13:a2:00:42:35:db:cb",
            sensor_id_non_drive="00:13:a2:00:42:30:83:0f",
            datafolder="data/CLP20241024data/Motor 7",
        ),
        "Motor 8": Motor(
            motor_name="Motor 8",
            sensor_id_drive="00:13:a2:00:42:35:db:cb",
            sensor_id_non_drive="00:13:a2:00:42:30:83:0f",
            datafolder="data/CLP20241024data/Motor 8",
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
    st.session_state["motor_rpm"] = 1488

if "sensor_fs" not in st.session_state:
    st.session_state["sensor_fs"] = 1600

# == Main == #

if not st.session_state["selected_motor"]:

    overview = Overview()
    overview.display()

if st.session_state["selected_motor"]:

    detail = Detail()
    detail.display()
