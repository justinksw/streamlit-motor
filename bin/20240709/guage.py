import plotly.graph_objects as go
import streamviz


def gauge():
    fig = go.Figure(

        go.Indicator(
            mode="gauge",
            value=100,
            domain={"x": [0, 1], "y": [0, 1]},
            # title={'text': "Speed"}
            gauge={
                "shape": "angular",
                "axis": {"range": [0, 600]},
                "bar": {"color": "darkblue"},  # color of the middle bar
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


# def gauge2():

#     layout = go.Layout(
#         autosize=False,
#         height=250,
#         margin=go.layout.Margin(l=30, r=30, b=1, t=1, pad=1)
#     )

#     return streamviz.gauge(0.75, layout)

# import streamlit as st
# import plotly.graph_objects as go

#         fig.add_trace(go.Indicator(
#             mode="gauge+number+delta",
#             title = {'text': "price"},
#             delta = {'reference': ask_price, 'relative': False, 'increasing': {'color': "RebeccaPurple"}, 'decreasing': {'color': "RoyalBlue"}},
#             value = current_price,
#             domain={'x': [0, 1], 'y': [0, 1]},
#             gauge={
#                 'shape': 'angular',
#                 'axis': {'range': [bid_price - spread, ask_price + spread]},
#                 #'axis': {'range': [lower_limit, upper_limit]},
#                 'bar': {'color': "darkblue"},
#                 'bgcolor': 'yellow',
#                 'borderwidth': 2,
#                 'bordercolor': 'black',
#                 'steps': [
#                     {'range': [bid_price*0.9 , bid_price], 'color': 'green'},
#                     {'range': [ask_price , ask_price*1.1], 'color': 'red'}
#                 ],
#                 'threshold': {
#                     'line': {'color': 'orange', 'width': 6},
#                     'thickness': 0.75,
#                     'value': current_price,
#                 }
#             },
#             #number={'prefix': 'BTC'}
#         ))

#         # Adjust the width and height of the gauge
#         #fig.update_layout(height=500, width=800)
#         with fig_placeholder:
#                 #st.plotly_chart(fig, theme="streamlit", use_container_width=True)
#                 st.plotly_chart(fig, use_container_width=True)
#                 #st.plotly_chart(fig)
