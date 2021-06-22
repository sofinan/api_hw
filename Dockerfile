FROM ubuntu:latest
RUN apt update -y
RUN apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools git wget nano mongodb -y
RUN pip install uwsgi flask pymongo requests prometheus-flask-exporter

ARG BRANCH

RUN mkdir app
RUN git clone -b $BRANCH https://github.com/sofinan/api_hw.git
WORKDIR api_hw

RUN wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

ENV dbname 'epam_hw'
ENV artistname 'The Beatles'
ENV colname 'main'

ENTRYPOINT uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
