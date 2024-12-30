from jinja2 import Template
import numpy as np
import pandas as pd

import streamlit as st

from src.plots import Plots


def generate_html_template():
    html_template = """
    <!DOCTYPE html>
    <html>
    
    <head>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                color: #272829;
                align-items: center;
                justify-content: center;
                margin: 20px 100px;
            }
            .header {
                text-align: center;
            }
            .logo{
                margin-top: 10px;
            }
            .logo-text{
                margin-top: 0px;
            }
            img {
                width: 400px;
            }
            .summary-table {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            table { 
                width: 50%;
                border-collapse: collapse;
                text-align: center;
            }
            th, td { 
                padding: 8px 12px;
                border: 1px solid #dddddd;
                text-align: center;
            }
            th { background-color: #f2f2f2; }
            .plotly-graph { text-align: center; }
        </style>
    </head>

    <body>
    
        <div class="header">
            <div class="logo">
                <img src="./materials/logo.png">
            </div>
            <h1 class="logo-text"> CAiRS Motor Guard Analysis Report </h1>
        </div>
     
        <div class="summary-table">
            {{table}}
        </div>
        
        <h2> {{name}} </h2>

        <div class="plotly-graph">
            {{raw_data_fig}} 
        </div>

        <div class="plotly-graph">
            {{fig2}} 
        </div>

    </body>

    </html>
    """

    template = Template(html_template)

    summary = pd.DataFrame(
        {
            "Motor": [
                "Motor1",
                "Motor2",
                "Motor3",
                "Motor4",
                "Motor5",
                "Motor6",
                "Motor7",
                "Motor8",
            ],
            "Condition": [
                "Health",
                "Health",
                "Health",
                "Health",
                "Health",
                "Health",
                "Health",
                "Health",
            ],
        }
    )

    # html_report = template.render(plotly_chart=fig.to_html(full_html=False))

    motor1 = st.session_state["motors"]["Motor 4"]
    motor1_name = motor1.get_motor_name()

    motor_data = motor1.get_data()
    idx = motor_data["Sensor Loc"].index("Drive-end")
    y = motor_data["Data"][idx]
    x = np.linspace(0, len(y), len(y)) / 1600

    plot = Plots([x], [y], [motor1_name], 1600)

    fig = plot.plot_fft_iftt()
    fig2 = plot.plot_fft(ref={})

    html_report = template.render(
        table=summary.to_html(index=False),
        name=motor1_name,
        raw_data_fig=fig.to_html(full_html=False),
        fig2=fig2.to_html(full_html=False),
    )

    return html_report


def generate_report():

    html_report = generate_html_template()

    with open("report.html", "w") as f:
        f.write(html_report)

    return True
