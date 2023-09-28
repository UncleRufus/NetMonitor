FROM python:3.10.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1\
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update -y && apt-get install -y \
    openssh-server \
    vim \
    tmux \
    iputils-ping \
    curl \
    python3-pip &&\
    pip install --upgrade pip &&\
    pip install poetry &&\
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN poetry config virtualenvs.create false &&\
    poetry export --without-hashes -f requirements.txt --output requirements.txt &&\
    pip install -r requirements.txt &&\
    yes | poetry cache clear --all .
