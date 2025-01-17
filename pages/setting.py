import streamlit as st

from src2.navigation import navigation

navigation()

st.title("Configurations")

container = st.container(border=True)
with container:
    st.subheader("Motor Operation Speed")

    input_motor_rpm = st.text_input("Rotation Speed [RPM]")
    if input_motor_rpm: 
        st.session_state["motor_rpm"] = input_motor_rpm

    st.write(f"Current Setting [RPM]: {st.session_state['motor_rpm']}")

container = st.container(border=True)
with container:
    st.subheader("Sensor Sampling Rate")

    input_sensor_fs = st.text_input("Sensor Sampling Rate [Hz]")
    if input_sensor_fs:
        st.session_state["sensor_fs"] = input_sensor_fs

    st.write(f"Current Setting [Hz]: {st.session_state['sensor_fs']}")
