# Local start

In Terminal:

> $ streamlit run streamlit_app.py


# Prerequisites

Development environment:

- Python 3.9.19
- Streamlit 1.36.0
- Pandas 2.2.2
- Plotly 5.22.0

To install required packages:

> $ pip install -r requirements.txt


# Project Architecture

```
. {root}
    |--- {.streamlit}
        |--- config.toml
        |--- secrets.toml
    |--- {data}
        |--- {Accelerometer}
            |--- xxxx.lvm
            |--- xxxx.lvm
            ...            
    |--- {materials}
        |--- logo1.png
    |--- {pages}
        |--- analysis.py
        |--- dashboard.py
        |--- developing.py
    |--- {plots}
        |--- gauge.py
    readme.md
    navigation.py
    streamlit_app.py
    requirements.txt
```

# References

## Streamlit APIs Documentation

https://docs.streamlit.io/

https://cheat-sheet.streamlit.app/


## Authentication

Adding an authentication component to your app

https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/

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


## Multi-page apps with widget state preservation

https://discuss.streamlit.io/t/multi-page-app-with-session-state/3074

https://discuss.streamlit.io/t/multi-page-apps-with-widget-state-preservation-the-simple-way/22303

https://github.com/streamlit/streamlit/issues/5813


## Database MySQL

Connect Streamlit to MySQL

https://docs.streamlit.io/develop/tutorials/databases/mysql

Get start MySQL

https://dev.mysql.com/doc/mysql-getting-started/en/

Install MySQL on MacOS

https://dev.mysql.com/doc/refman/8.0/en/macos-installation-launchd.html

Install and use MySQL launch daemon on MacOS

https://dev.mysql.com/doc/refman/8.0/en/macos-installation-launchd.html


MySQL Workbench

https://dev.mysql.com/doc/workbench/en/


# Database

## Install MySQL on MacOS

### 1. 確認要安裝的版本

> $ brew info mysql

### 2. 安裝預設的版本

> $ brew install mysql mycli

如果要安裝特定的版本：

> $ brew install mysql@5.7 mycli

查詢 homebrew 提供的版本：

https://formulae.brew.sh/formula/mysql

## 啟動 / 結束 MySQL

### 1. 確認目前 MySQL 的執行狀態

> $ brew services list

### 2. 啟動 MySQL

> $ brew services start mysql

### 3. 結束 MySQL

> $ brew services stop mysql

## 登入 MySQL

> $ mycli -u root -h localhost

homebrew 安裝的 MySQL 預設會跑在 localhost


Ref: https://myapollo.com.tw/blog/install-mysql-using-homebrew/


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


