# import pandas as pd

# import streamlit as st

# from src2.navigation import navigation

# navigation()

# st.write("")

# col1, col2 = st.columns([0.2, 0.8], gap="large", vertical_alignment="top")

# with col1:
#     option = st.selectbox(
#         label="Choose a label",
#         options=("lub100", "lub75", "lub25", "lub10", "lub2_5"),
#     )

# conn = st.connection("mysql", type="sql")
# query = f"SELECT * FROM lub WHERE label='{option}';"

# table = conn.query(query, ttl=0)
# df = pd.DataFrame(table)

# with col2:
#     st.dataframe(df.head(50))
