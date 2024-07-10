# Local start

In Terminal:

> streamlit run streamlit_app.py


# Prerequisites

Development environment:

- Python 3.9.19
- Streamlit 1.36.0
- Pandas 2.2.2
- Plotly 5.22.0

To install required packages:

> pip install -r requirements.txt


# Project Architecture

```
. {root}
    |--- {data}
        |--- {Accelerometer}
            |--- xxxx.lvm
            |--- xxxx.lvm
            ...            
    |--- {materials}
        |--- logo.png
    |--- {pages}
        |--- analysis.py
        |--- dashboard.py
        |--- developing.py
    |--- {plots}
        |--- gauge.py
    readme.md
    streamlit_app.py
```


# Streamlit APIs Documentation

https://docs.streamlit.io/


# References

## Authentication

Demo-project of a multipage app with authentication

https://github.com/blackary/streamlit-login?tab=readme-ov-file

Streamlit Authentication without SSO

https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso

SSO (Single Sign-On 單一登入)

https://aws.amazon.com/tw/what-is/sso/


## Sidebar

https://discuss.streamlit.io/t/specify-sidebar-width/45866


## Gauge indicator

https://discuss.streamlit.io/t/plotly-gauge-overwriting-itself/46651

https://stackoverflow.com/questions/69072792/how-to-add-legends-on-gauge-chart-using-plotly-graph-object

https://plotly.com/python-api-reference/generated/plotly.graph_objects.indicator.html

https://plotly.com/python/indicator/






