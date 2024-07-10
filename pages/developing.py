import streamlit as st
import plotly.graph_objects as go
from navigation import navigation

navigation()

# st.set_page_config(layout='wide')

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=270,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Speed"}))


col1, col2, col3 = st.columns(3, vertical_alignment="center")

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.plotly_chart(fig, use_container_width=True)

with col3:
    uploaded_file = st.file_uploader(
        label="Upload **One** File", label_visibility="visible",)
