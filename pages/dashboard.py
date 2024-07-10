import datetime

import pandas as pd
import streamlit as st

from plots.guage import gauge

# This is the main page of the dashboard

st.set_page_config(layout='wide')

datetime_now = datetime.date.today()
datetime_now

LAST_INSPECTION_DATE = datetime.date(2024, 7, 1)

DIFF = abs(datetime_now - LAST_INSPECTION_DATE).days


@st.cache_data
def get_data(uploaded_file):
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    return dataframe


# == Motor Selection == #

motorSelectionContainer = st.container(height=None, border=True)

with motorSelectionContainer:

    motorSelection = st.selectbox(
        label="Select a motor for inspection.",
        options=[
            "Motor 1",
            "Motor 2",
        ],
        index=0,
    )
    # st.write(f"**{motorSelection}** is selected.")


# == Key Metrics == #

keyMetricsContainer = st.container(height=None, border=True)
with keyMetricsContainer:
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Motor", value=f"{motorSelection}")
    col2.metric(label="Condition", value="Good")
    col3.metric(label="Since last inspection", value=f"{DIFF} day(s)")


# == Key Indicator == #

keyIndicatorContainer = st.container(height=None, border=True)
with keyIndicatorContainer:

    col1, col2 = st.columns(
        [6, 6], vertical_alignment="top", gap="medium")

    with col1:
        st.plotly_chart(gauge(), use_container_width=True)
        # gauge()

    with col2:
        st.plotly_chart(gauge(), use_container_width=True)
        # gauge()


# == Data Visualization == #

container = st.container(height=None, border=True)

with container:
    uploaded_file = st.file_uploader(
        label="Upload **One** File", label_visibility="visible")

if uploaded_file is not None:
    uploaded_dataframe = get_data(uploaded_file)

    df = uploaded_dataframe[["角度X(°)", "角度Y(°)", "角度Z(°)"]].head(100)
    st.line_chart(df)
