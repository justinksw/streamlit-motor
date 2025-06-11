from time import sleep

import streamlit as st

from src.report import generate_report


def navigation():

    if not st.session_state.get("password_correct", False):
        st.switch_page("streamlit_app.py")

    with st.sidebar:
        # st.markdown(
        #     """
        #     <style>
        #         section[data-testid="stSidebar"] {
        #             width: 500px;
        #             align-items: center;
        #         }
        #     </style>
        #     """,
        #     unsafe_allow_html=True,
        # )

        logo = "materials/logo.png"
        st.logo(
            logo,
        )  # icon_image=logo

        # THIS markdown is used for changing the style of the logo
        st.markdown(
            """
            <style>
                div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
                    height: 4rem;
                    width: auto;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # THIS markdown is used as Title text
        st.markdown(
            """
            <style>
                .title{
                    color: #752303;
                    font-size: 33px;
                }
            </style>

            <p class="title"> Dashboard </p>
            """,
            unsafe_allow_html=True,
        )

        # st.title("MotorGuard")

        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            # st.markdown('<span style="font-size: 24px;"><a href="#health-condition-indicator" style="text-decoration: none; color: black">Header</a></span>', unsafe_allow_html=True)

            st.page_link("pages/setting.py", label="Setting")
            st.page_link("pages/index.py", label="Current Status")
            st.page_link("pages/ai_diagnosis.py", label="AI Diagnosis")
            st.page_link("pages/offline_analysis.py", label="Offline Analysis")
            st.page_link("pages/historical_trend.py", label="Historical Trend")
            st.page_link("pages/about.py", label="About")

            st.write("")
            st.write("")

            genre = st.radio(
                label="Data",
                options=["Acceleration", "Velocity"],
                label_visibility="hidden",
                index=0,
            )
            if genre == "Acceleration":
                st.session_state["data_type"] = "Acceleration"
            else:
                st.session_state["data_type"] = "Velocity"

            st.write("")
            st.write("")

            # In Streamlit, the default type of button is "secondary"
            st.markdown(
                """
                <style>
                    button[kind="primary"] {
                            color: black;
                            background-color: #F0F2F6;
                            border: solid;
                            border-color: #CFCFD2;
                            border-width: thin;
                            margin: 10px;
                            font-family: sans-serif;
                        }
                    button[kind="primary"]:hover{
                            background-color: #E2E7EF;
                        }
                </style>
                """,
                unsafe_allow_html=True,
            )

            report = st.button(
                "Report",
                use_container_width=True,
                on_click=generate_report,
                type="primary",
            )

            if st.button(
                "Log out",
                use_container_width=True,
                type="primary",
            ):
                logout()

            if report:
                st.success("Report generated")

    return True


def logout():
    st.session_state.logged_in = False
    del st.session_state["password_correct"]

    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("streamlit_app.py")
