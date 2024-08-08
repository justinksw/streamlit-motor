# Local start

In Terminal:

> $ streamlit run streamlit_app.py


# Prerequisites

Development environment:

- Python 3.9.19
- Streamlit 1.36.0
- Pandas 2.2.2
- Plotly 5.22.0

- kswutils

To install required packages:

> $ pip install -r requirements.txt


# Project Architecture

```
.{root}
|--- {.streamlit}
    |--- config.toml
    |--- secrets.toml
|--- {data} 
|--- {materials}
    |--- logo1.png
|--- {pages}
    |--- analysis.py
    |--- dashboard.py
    |--- developing.py
|--- {plots}
    |--- gauge.py
|--- readme.md
|--- navigation.py
|--- streamlit_app.py
|--- requirements.txt
```

# References

## Streamlit APIs Documentation

https://docs.streamlit.io/

https://cheat-sheet.streamlit.app/


## Authentication

- [Adding an authentication component to your app](https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/)

- [Demo-project of a multipage app with authentication](https://github.com/blackary/streamlit-login?tab=readme-ov-file)

- [Streamlit Authentication without SSO](https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso)

- [What is SSO (Single Sign-On)](https://aws.amazon.com/tw/what-is/sso/)


## Sidebar

- [Specify Sidebar Width](https://discuss.streamlit.io/t/specify-sidebar-width/45866)


## Container

- [Stylable container](https://arnaudmiribel.github.io/streamlit-extras/extras/stylable_container/)
- [Apply custom css to manually created container (Modify the CSS by ID)](https://discuss.streamlit.io/t/applying-custom-css-to-manually-created-containers/33428/1) 


## Button

- [How to style a button in streamlit](https://stackoverflow.com/questions/69478972/how-to-style-a-button-in-streamlit)


## Gauge indicator

- [Config the Plotly gauge indicator](https://discuss.streamlit.io/t/plotly-gauge-overwriting-itself/46651)

- [Modify tick style of Plotly gauge indicator](https://stackoverflow.com/questions/69072792/how-to-add-legends-on-gauge-chart-using-plotly-graph-object)

- [Plotly Python Indicator](https://plotly.com/python/indicator/)

- [Plotly Graph Objects Indicator](https://plotly.com/python-api-reference/generated/plotly.graph_objects.indicator.html)

- [JS Gauge Indicator](https://www.cssscript.com/customizable-gauge-canvas/)


## Battery

- [Battery Status](https://tutorials-warehouse.blogspot.com/2023/03/display-battery-status-using-html-css.html)

## Percentage

- [Codepen Percentage Circle](https://codepen.io/sergiopedercini/pen/jmKdbj)


## Multi-page apps with widget state preservation

- [Multipage App with session state](https://discuss.streamlit.io/t/multi-page-app-with-session-state/3074)

- [Multipage App with widget state preservation](https://discuss.streamlit.io/t/multi-page-apps-with-widget-state-preservation-the-simple-way/22303)

- [Issues 5813](https://github.com/streamlit/streamlit/issues/5813)


## Database MySQL

- [Connect Streamlit to MySQL](https://docs.streamlit.io/develop/tutorials/databases/mysql)

- [Get start MySQL](https://dev.mysql.com/doc/mysql-getting-started/en/)

- [Install MySQL on MacOS](https://dev.mysql.com/doc/refman/8.0/en/macos-installation-launchd.html)

- [Install and use MySQL launch daemon on MacOS](https://dev.mysql.com/doc/refman/8.0/en/macos-installation-launchd.html)

- [MySQL Workbench](https://dev.mysql.com/doc/workbench/en/)


# Database

## Install MySQL on MacOS

### 1. Check the version

> $ brew info mysql

### 2. Install default version

> $ brew install mysql mycli

Install specific version

> $ brew install mysql@5.7 mycli

Check versions in Homebrew

https://formulae.brew.sh/formula/mysql

## Start / Stop MySQL

### 1. Check MySQL Status

> $ brew services list

### 2. Start MySQL

> $ brew services start mysql

### 3. Stop MySQL

> $ brew services stop mysql

## Log-in MySQL

> $ mycli -u root -h localhost


Ref: [Install mysql using homebrew](https://myapollo.com.tw/blog/install-mysql-using-homebrew/)


# Connection between MySQL and Streamlit

## 1. Download Python MySQL connector

> $ pip install mysql-connector
> $ pip install SQLAlchemy

## 2. Local host

### dashboard.py

```
conn = st.connection('mysql', type='sql')
data = conn.query("select * from imu;", ttl=600)
df = pd.DataFrame(data)
st.dataframe(df)
```

### secrets.toml

```
[connections.mysql]
dialect = "mysql"
host = "localhost"
port = 3306
database = "test_schema"
username = "root"
password = ""
```

**IMPORTANT**

.gitignore the secrects.toml


