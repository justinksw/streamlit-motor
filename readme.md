# Dashboard for motor monitoring

This dashboard is a web-app built mainly in Python and JavaScript under the Streamlit framework.

Functionality:

- Visualize the sensor data, which is stored in MySQL database.
- Support the signal processing calculation, including Fourier analysis and signal feature extraction.
- Support a AI model (in Pytorch), variational autoencoder (VAE), which is used for anomaly detection.

This project is for demo purpose.

![image1](https://github.com/justinksw/streamlit-motor/blob/main/demo%20/1.png)

![image1](https://github.com/justinksw/streamlit-motor/blob/main/demo%20/2.png)


# Local start

In Terminal:

> $ streamlit run streamlit_app.py


# Prerequisites

Development environment:

- Python
- Streamlit
- Pandas
- Plotly
- Pytorch
- Scikit-learn
- librosa
- numpy
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
    |--- {vae}
    |--- logo.png
|--- {pages}
    |--- about.py
    |--- historical_trend.py
    |--- index.py
    |--- offline_analysis.py
|--- {pages2}
    |--- detail.py
    |--- overview.py
|--- {src}
    |--- components.py
|--- {src2}
    |--- navigation.py
|--- readme.md
|--- streamlit_app.py
|--- requirements.txt
```

# References

## Streamlit APIs Documentation

- [Streamlit](https://docs.streamlit.io/)

- [Cheat sheet](https://cheat-sheet.streamlit.app/)


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

- [Button CSS for streamlit](https://discuss.streamlit.io/t/button-css-for-streamlit/45888/4)

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


## Remove MySQL on Mac via HomeBrew

https://cloud.baidu.com/article/3301864

**!NOTE: DO NOT TRY TO INSTALL NEW VERSION OF SQL BY NO REASON**


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


## Docker Image

- [Deploy Streamlit using Docker](https://docs.streamlit.io/deploy/tutorials/docker)
- [Fails on mysqlclient installation](https://stackoverflow.com/questions/76533384/docker-alpine-build-fails-on-mysqlclient-installation-with-error-exception-can)
- [Fails for h5py in python 3.9](https://stackoverflow.com/questions/78359706/docker-build-fails-for-h5py-in-python-3-9)
- [apt-get install libsndfile1](https://stackoverflow.com/questions/55086834/cant-import-soundfile-python)

### 0. Pip freeze

> $ pip list --format=freeze > requirements.txt

### 1. Check Docker installation

> $ docker --version

### 2. Prepare the `Dockerfile`

### 3. Build Docker image

> $ docker build -t streamlit .

### 4. List the Docker image

> $ docker images

### 5. Run Streamlit via Docker

> $ docker run -p 8501:8501 streamlit


## Streamlit + MySQL

> $ docker run --name docker_mysql -p 3307:3306 -e MYSQL_ROOT_PASSWORD=xxxxxx -d mysql

> $ docker-compose up -d

## Docker Image Save and Load

Window:

```
docker load -i windowsservercore.tar
```

## Docker Container Export and Import


## Bind local folder with the direcotry in docker

```
docker run -v /Users/justin/GitHub/streamlit-motor/data/CLP20241024data/Motor_4:/streamlit-motor/data -p 8501:8501 streamlit
```

[Exploring Docker container's file system](https://stackoverflow.com/questions/20813486/exploring-docker-containers-file-system)

[How can I use a local file on container?](https://stackoverflow.com/questions/44876778/how-can-i-use-a-local-file-on-container)
