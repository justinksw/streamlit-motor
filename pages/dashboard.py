import datetime

import pandas as pd
import streamlit as st

from navigation import navigation
from plots.guage import gauge


navigation()

conn = st.connection('mysql', type='sql')
data = conn.query("select * from imu;", ttl=600)
df = pd.DataFrame(data)
st.dataframe(df)

#

datetime_now = datetime.date.today()
datetime_now

LAST_INSPECTION_DATE = datetime.date(2024, 7, 1)

DIFF = abs(datetime_now - LAST_INSPECTION_DATE).days





# == Motor Selection == #

motorSelectionContainer = st.container(height=None, border=True)

with motorSelectionContainer:

    motorSelection = st.selectbox(
        label="Select a motor for inspection.",
        options=[
            "Motor 1",  # 100% lubricant data
            "Motor 2",  # 75% lubricant data
            "Motor 3",  # 25% lubricant data
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



