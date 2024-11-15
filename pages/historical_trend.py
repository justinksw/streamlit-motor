import numpy as np
import pandas as pd
import streamlit as st

from src.anlysis import Analysis
from src.motor import MotorJsonFile
from src2.navigation import navigation

from kswutils_plotly.plotly_graph import PlotlyGraph


navigation()


class Historical:
    def __init__(self):

        motors = st.session_state["motors"]

        col1, col2, col3 = st.columns(3)

        with col1:
            motor_selection = st.selectbox("Motor", motors.keys(), index=3)
        with col2:
            sensor_loc = st.selectbox("Sensor", ["Drive-end", "Non-drive-end"])
        with col3:
            data_type = st.selectbox("Data", ["RMS Z", "Battery"])

        motor = motors[motor_selection]

        df = motor.get_historical_data()
        df = pd.DataFrame(df)

        df2 = df[df["Sensor Loc"] == sensor_loc]

        X = df2["TS HK"]
        Y = df2[data_type]

        G = PlotlyGraph()
        G.add_line(
            x=X,
            y=Y,
            title=f"{motor_selection}: {sensor_loc}",
            xlabel="Time",
            ylabel="Value",
            # xticks_val=_x.tolist(),
            # xticks_label=dff["time"],
            mode="lines+markers",
        )

        selection = st.plotly_chart(G.fig, on_select="rerun")

        if selection["selection"]["points"]:
            filename = df2[df2["TS HK"] == selection["selection"]["points"][0]["x"]][
                "File Name"
            ].iloc[0]

            path = f"{motor.datafolder}/{filename}.json"

            files = [path]

            fs = 1600
            if motor_selection not in ["Motor 4", "Motor 7", "Motor 8"]:
                fs = 50000

            datafiles = [MotorJsonFile(i, local=True) for i in files]

            Y = []
            X = []
            labels = []

            for m in datafiles:

                _y = m.get_data()
                _x = np.linspace(0, len(_y), len(_y)) / fs

                Y.append(_y)
                X.append(_x)
                labels.append(m.get_file_name())

            analysis = Analysis()
            analysis.plot_charts(X, Y, labels, fs)


history = Historical()
