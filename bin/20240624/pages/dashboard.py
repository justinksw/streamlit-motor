import pandas as pd

import streamlit as st

import plotly.graph_objects as go

from plots.guage import gauge


st.set_page_config(layout='wide')


# == Function == #

@st.cache_data
def get_data(uploaded_file):
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    return dataframe


# == Contain == #

with st.container(border=True):

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


# == Container == #

with st.container(border=True):

    col1, col2 = st.columns(
        [6, 6], vertical_alignment="top", gap="medium")

    with col1:
        subcol1, subcol2 = st.columns([6, 6], vertical_alignment="top")

        with subcol1:
            st.plotly_chart(gauge(), use_container_width=True)

        with subcol2:
            st.plotly_chart(gauge(), use_container_width=True)

    with col2:
        uploaded_file = st.file_uploader(
            label="Upload **One** File", label_visibility="visible")


with st.container(border=True):

    if uploaded_file is not None:
        uploaded_dataframe = get_data(uploaded_file)

        df = uploaded_dataframe[["角度X(°)", "角度Y(°)", "角度Z(°)"]].head(100)
        st.line_chart(df)
