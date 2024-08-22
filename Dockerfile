FROM python:3.9-slim

RUN pip3 install --upgrade pip

WORKDIR /streamlit-motor

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libhdf5-dev \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install --no-binary h5py h5py

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
