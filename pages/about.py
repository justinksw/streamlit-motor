import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container

from src2.navigation import navigation

navigation()

st.write("This is a dashboard")