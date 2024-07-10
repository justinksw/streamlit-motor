import plotly.graph_objects as go


def gauge():
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=270,
            domain={'x': [0, 1], 'y': [0, 1]},
            # title={'text': "Speed"}
        ),
        layout=go.Layout(
            autosize=False,
            height=150,
            margin=go.layout.Margin(l=20, r=20, b=1, t=1, pad=1)
        ),
    )

    return fig
