from time import sleep

import streamlit as st


def make_navigation():

    if not st.session_state.get("password_correct", False):
        st.switch_page("streamlit_app.py")

    with st.sidebar:
        # st.markdown(
        #     """
        #     <style>
        #         section[data-testid="stSidebar"] {
        #             width: 500px !important; # Set the width to your desired value
        #         }
        #     </style>
        #     """,
        #     unsafe_allow_html=True,
        # )

        st.title("Dashboard")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):

            st.page_link("pages/dashboard.py",
                         label="Overview")

            st.page_link("pages/analysis.py",
                         label="Analysis")

            st.page_link("pages/developing.py",
                         label="Developing")

            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

    return True


def logout():
    st.session_state.logged_in = False
    del st.session_state["password_correct"]

    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("streamlit_app.py")
