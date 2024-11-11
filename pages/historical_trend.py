import pytz
from datetime import date, datetime, timedelta

import streamlit as st
import pandas as pd

from src2.navigation import navigation
from model_motor.motor import get_historical_data

from pages.do_anlysis import Analysis

from kswutils_plotly.plotly_graph import PlotlyGraph


navigation()


if "date_now" not in st.session_state:
    st.session_state.date_now = datetime.now()

if "selections" not in st.session_state:
    st.session_state.selections = None

start_date = datetime(2024, 10, 1)
# end_date = datetime.now()  # THIS NOT WORK
end_date = st.session_state["date_now"]


selected_date = st.slider(
    "Select a date range",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    step=timedelta(days=1),
)

st.write(selected_date)

df = get_historical_data("data/CLP20241024data/Motor 4")

df = pd.DataFrame(df)

# df["TS HK"] = pd.to_datetime(df["TS HK"])

# df = df[
#     (df["TS HK"] > selected_date[0]) & (df["TS HK"] < selected_date[1])
# ]

# df

opt_sensor_id = df["Sensor ID"].unique().tolist()
opt_plt = ["RMS X", "RMS Y", "RMS Z", "Battery"]

select_id = st.selectbox("Sensor ID", opt_sensor_id)
select_plt = st.selectbox("Sensor ID", opt_plt)

df2 = df[df["Sensor ID"] == select_id]

X = df2["TS HK"]
Y = df2[select_plt]

# st.line_chart(df2, x="TS HK", y=select_plt)

G = PlotlyGraph()

G.add_line(X, Y)

G.add_line(
    x=X,
    y=Y,
    title=f"Sensor ID: {select_id}",
    xlabel="Time",
    ylabel="Value",
    # xticks_val=_x.tolist(),
    # xticks_label=dff["time"],
    mode="lines+markers",
)

selection = st.plotly_chart(G.fig, on_select="rerun")

# st.write(selection)

if selection["selection"]["points"]:

    filename = df2[df2["TS HK"] == selection["selection"]["points"][0]["x"]][
        "File Name"
    ].iloc[0]

    path = f"data/CLP20241024data/Motor 4/{filename}.json"

    files = [path]

    analysis = Analysis(files, local=True)
    analysis.display()

df2
