FROM ubuntu:latest
RUN apt update -y
RUN apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools git wget nano mongodb cron -y
RUN pip install uwsgi flask pymongo requests prometheus-flask-exporter

RUN mkdir app
RUN git clone https://github.com/sofinan/api_hw.git
WORKDIR api_hw

RUN wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

ENV dbname 'epam_hw'
ENV artistname 'The Beatles'
ENV colname 'main'

RUN env > envvars
RUN systemctl start cron

ENTRYPOINT uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
