import pandas as pd

import streamlit as st

from plots.guage import gauge


st.set_page_config(layout='wide')


@st.cache_data
def get_data(uploaded_file):
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    return dataframe

container = st.container(height=None, border=True)

with container:

    model = st.radio(
        label="Select a model.",
        options=[
            "Motor 1",
            "Motor 2",
        ],
        index=None,
        horizontal=True,
    )
    st.write(f"**{model}** is selected.")


def row2():
    container = st.container(height=None, border=True)

    with container:

        col1, col2 = st.columns(
            [6, 6], vertical_alignment="top", gap="medium")

        with col1:
            st.plotly_chart(gauge(), use_container_width=True)
            # gauge()

        with col2:
            st.plotly_chart(gauge(), use_container_width=True)
            # gauge()


def row3():
    container = st.container(height=None, border=True)

    with container:
        uploaded_file = st.file_uploader(
            label="Upload **One** File", label_visibility="visible")

    return uploaded_file


row2()
uploaded_file = row3()


if uploaded_file is not None:
    uploaded_dataframe = get_data(uploaded_file)

    df = uploaded_dataframe[["角度X(°)", "角度Y(°)", "角度Z(°)"]].head(100)
    st.line_chart(df)
