import plotly.graph_objects as go
import streamviz


def gauge(title="indicator"):

    fig = go.Figure(

        go.Indicator(
            mode="gauge",
            value=100,
            domain={"x": [0, 1], "y": [0, 1]},
            title={'text': "Indicator"},
            gauge={
                "shape": "angular",
                "axis": {
                    "range": [0, 600],
                    "visible": True,
                    "tickmode": "array",
                    "tickvals": [100, 300, 500],
                    "ticktext": ["Good", "Warn", "Danger"],
                    "ticks": "",
                },
                "bar": {"color": "black"},  # color of the middle bar
                "bgcolor": "white",  # background color of the middle bar
                "borderwidth": 1,  # line weight of border of the middle bar
                "bordercolor": "black",  # line color of the border of the middle bar
                "steps": [
                    {"range": [0, 200], "color": "green"},
                    {"range": [200, 400], "color": "yellow"},
                    {"range": [400, 600], "color": "red"},
                ],
                # "threshold": {
                #     "line": {"color": "orange", "width": 5},
                #     "thickness": 0.8,
                #     "value": 450,
                # }
            }
        ),

        layout=go.Layout(
            autosize=False,
            height=250,
            margin=go.layout.Margin(l=30, r=30, b=1, t=1, pad=1)
        ),
    )

    return fig
