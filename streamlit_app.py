from time import sleep

import streamlit as st

from src.login import login


if not login():
    st.stop()

else:
    st.session_state.logged_in = True
    st.success("Logged in successfully!")
    sleep(0.5)
    st.switch_page("pages/dashboard.py")

#

# st.session_state["password_correct"] = True
# st.session_state.logged_in = True
# st.success("Logged in successfully!")
# sleep(0.5)
# st.switch_page("pages/dashboard.py")
