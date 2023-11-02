FROM python:3.11.4

ENV env 1

WORKDIR /usr/src/manager

COPY requirements.txt ./

RUN pip install -r requirements.txt
