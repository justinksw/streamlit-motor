import streamlit as st
from datetime import datetime, timedelta

# Create a datetime slider with a range of one week
start_date = datetime(2020, 1, 1)
end_date = start_date + timedelta(weeks=1)

selected_date = st.slider(
    "Select a date range",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    step=timedelta(days=1),
)
