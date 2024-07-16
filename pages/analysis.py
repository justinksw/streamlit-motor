import streamlit as st

from navigation import navigation

navigation()


@st.cache_data
def get_data(uploaded_file):
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    return dataframe


container = st.container(height=None, border=True)

with container:
    uploaded_file = st.file_uploader(
        label="Upload a CSV / Excel File", label_visibility="visible")

if uploaded_file is not None:
    uploaded_dataframe = get_data(uploaded_file)

    df = uploaded_dataframe[["角度X(°)", "角度Y(°)", "角度Z(°)"]].head(100)
    st.line_chart(df)
