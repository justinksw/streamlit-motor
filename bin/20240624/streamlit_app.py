import streamlit as st

dashboard = st.Page("pages/dashboard.py", title="Overview", default=True)
analysis_page = st.Page("pages/analysis.py", title="Analysis")

developing = st.Page("pages/developing.py", title='Developing')

pg = st.navigation(
    {
        "Dashboard": [dashboard, analysis_page, developing]
    },
    position="sidebar"
)

pg.run()
