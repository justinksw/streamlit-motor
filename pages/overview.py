import random

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from src.components import Static
from model_motor.motor import Motor


STATIC = Static()


class Overview:
    def __init__(self) -> None:

        self.motors = [
            Motor(
                motor_name="Motor 1",
                sensor_id_drive="NA",
                sensor_id_non_drive="NA",
                datafolder="NA",
            ),
            Motor(
                motor_name="Motor 2",
                sensor_id_drive="NA",
                sensor_id_non_drive="NA",
                datafolder="NA",
            ),
            Motor(
                motor_name="Motor 3",
                sensor_id_drive="NA",
                sensor_id_non_drive="NA",
                datafolder="NA",
            ),
            Motor(
                motor_name="Motor 4",
                sensor_id_drive="00:13:a2:00:42:35:db:cb",
                sensor_id_non_drive="00:13:a2:00:42:30:83:0f",
                datafolder="data/CLP20241024data/Motor 4",
            ),
            Motor(
                motor_name="Motor 5",
                sensor_id_drive="NA",
                sensor_id_non_drive="NA",
                datafolder="NA",
            ),
            Motor(
                motor_name="Motor 6",
                sensor_id_drive="NA",
                sensor_id_non_drive="NA",
                datafolder="NA",
            ),
            Motor(
                motor_name="Motor 7",
                sensor_id_drive="00:13:a2:00:42:35:db:cb",
                sensor_id_non_drive="00:13:a2:00:42:30:83:0f",
                datafolder="data/CLP20241024data/Motor 4",
            ),
            Motor(
                motor_name="Motor 8",
                sensor_id_drive="00:13:a2:00:42:35:db:cb",
                sensor_id_non_drive="00:13:a2:00:42:30:83:0f",
                datafolder="data/CLP20241024data/Motor 4",
            ),
        ]

    def infomation(self, motor):

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

                STATIC.infomation_card(
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
                        button {
                            color: black;
                            background-color: #F0F2F6;
                            border: none;
                            margin: 10px;
                            font-family: sans-serif;
                        }

                        button:hover{
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
                    self.infomation(self.motors[0])
                    self.infomation(self.motors[2])
                    self.infomation(self.motors[4])
                    self.infomation(self.motors[6])

                with col2:
                    self.infomation(self.motors[1])
                    self.infomation(self.motors[3])
                    self.infomation(self.motors[5])
                    self.infomation(self.motors[7])

        return None


def select_motor(id):
    st.session_state.selected_motor = id
    return None
