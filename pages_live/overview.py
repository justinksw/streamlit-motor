import random

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from src.components import Static


STATIC = Static()


class Overview:
    def __init__(self) -> None:
        pass

    def infomation_card(self, name, id):

        if id == "Motor 1":
            battery1 = int(random.random() * 100)
            battery2 = int(random.random() * 100)
            condition = "Health"
            _color = "#4CC790"

        if id == "Motor 2":
            battery1 = int(random.random() * 100)
            battery2 = int(random.random() * 100)
            condition = "Warn"
            _color = "#FAFF02"

        if id == "Motor 3":
            battery1 = int(random.random() * 100)
            battery2 = int(random.random() * 100)
            condition = "Warn"
            _color = "#FAFF02"

        if id == "Motor 4":
            battery1 = int(random.random() * 100)
            battery2 = int(random.random() * 100)
            condition = "Warn"
            _color = "#FAFF02"

        if id == "Motor 5":
            battery1 = int(random.random() * 100)
            battery2 = int(random.random() * 100)
            condition = "Danger"
            _color = "#FAFF02"

        if id == "Motor 6":
            battery1 = 0
            battery2 = 0
            condition = "Unknown"
            _color = "#FAFF02"

        if id == "Motor 7":
            battery1 = 0
            battery2 = 0
            condition = "Unknown"
            _color = "#E6E6E6"

        if id == "Motor 8":
            battery1 = 0
            battery2 = 0
            condition = "Unknown"
            _color = "#E6E6E6"

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

                STATIC.infomation_card(name, condition, battery1, battery2)

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
                        key=id,
                        on_click=select_motor,
                        args=[id],
                    )

        return None

    def display(self):

        if not st.session_state.selected_motor:

            container1 = st.container(height=None, border=None)

            with container1:

                col1, col2 = st.columns(2)

                with col1:
                    self.infomation_card(name="Motor 1", id="Motor 1")
                    self.infomation_card(name="Motor 3", id="Motor 3")
                    self.infomation_card(name="Motor 5", id="Motor 5")
                    self.infomation_card(name="Motor 7", id="Motor 7")

                with col2:
                    self.infomation_card(name="Motor 2", id="Motor 2")
                    self.infomation_card(name="Motor 4", id="Motor 4")
                    self.infomation_card(name="Motor 6", id="Motor 6")
                    self.infomation_card(name="Motor 8", id="Motor 8")

        return None


def select_motor(id):
    st.session_state.selected_motor = id
    return None
