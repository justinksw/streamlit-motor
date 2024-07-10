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

# References

## Streamlit APIs Documentation

https://docs.streamlit.io/


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

Config the Plotly gauge indicator

https://discuss.streamlit.io/t/plotly-gauge-overwriting-itself/46651

Modify tick style of Plotly gauge indicator

https://stackoverflow.com/questions/69072792/how-to-add-legends-on-gauge-chart-using-plotly-graph-object

Plotly Indicator

https://plotly.com/python/indicator/

https://plotly.com/python-api-reference/generated/plotly.graph_objects.indicator.html


## Database MySQL

Connect Streamlit to MySQL

https://docs.streamlit.io/develop/tutorials/databases/mysql

Get start MySQL

https://dev.mysql.com/doc/mysql-getting-started/en/

Install MySQL on MacOS

https://dev.mysql.com/doc/refman/8.0/en/macos-installation-launchd.html

Install and use MySQL launch daemon on MacOS

https://dev.mysql.com/doc/refman/8.0/en/macos-installation-launchd.html

