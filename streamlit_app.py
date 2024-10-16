from time import sleep

import streamlit as st

from src2.login import login


st.set_page_config(
    layout="wide",
    page_title="CAiRS Motor"
)


# ==== #

login()

# ==== #

# st.session_state["password_correct"] = True
# st.session_state.logged_in = True
# st.success("Logged in successfully!")
# sleep(0.5)
# st.switch_page("pages/index.py")
