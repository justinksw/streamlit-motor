import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from src.components import Static
from src.motor import Motor


class Overview:
    def __init__(self) -> None:

        self.motors = st.session_state.motors

    def infomation(self, motor):

        static = Static()

        # Not worked. This will change all components.
        # st.markdown(
        #     """
        #     <style>
        #         div[data-testid="stVerticalBlockBorderWrapper"] {
        #             background-color: black;
        #         }
        #     </style>
        #     """,
        #     unsafe_allow_html=True,
        # )

        with stylable_container(
            key="info_card",
            css_styles="""
                {
                    background-color: #F0F2F6;
                    border-radius: 20px;
                }
                """,
        ):

            col1, col2 = st.columns([0.65, 0.35], vertical_alignment="center")

            with col1:

                static.infomation_card(
                    motor_name=motor.get_motor_name(),
                    motor_condition=motor.get_condition(),
                    battery1=motor.get_battery()[0],
                    battery2=motor.get_battery()[1],
                    inspection_date=motor.get_last_inspection_date(),
                )

            with col2:

                with stylable_container(
                    key="select_motor",
                    css_styles="""
                        button[kind="secondary"] {
                            color: black;
                            background-color: #F0F2F6;
                            border: none;
                            margin: 10px;
                            font-family: sans-serif;
                        }

                        button[kind="secondary"]:hover{
                            transform: scale(1.25);
                        }
                        """,
                ):

                    st.button(
                        "**Show Detail**",
                        key=motor.get_motor_name(),
                        on_click=select_motor,
                        args=[motor.get_motor_name()],
                    )

        return None

    def display(self):

        if not st.session_state.selected_motor:

            container1 = st.container(height=None, border=None)

            with container1:

                col1, col2 = st.columns(2)

                with col1:
                    self.infomation(self.motors["Motor 1"])
                    self.infomation(self.motors["Motor 3"])
                    self.infomation(self.motors["Motor 5"])
                    self.infomation(self.motors["Motor 7"])

                with col2:
                    self.infomation(self.motors["Motor 2"])
                    self.infomation(self.motors["Motor 4"])
                    self.infomation(self.motors["Motor 6"])
                    self.infomation(self.motors["Motor 8"])

        return None


def select_motor(id):
    st.session_state.selected_motor = id
    return None
