FROM ubuntu:latest
RUN apt update -y
RUN apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools git -y
RUN pip install uwsgi flask pymongo requests

RUN mkdir app
RUN git clone https://github.com/sofinan/api_hw.git
WORKDIR api_hw

ENV dbname 'epam_hw'
ENV artistName 'The Beatles'
ENV colname 'main'
ENV connstr 'mongodb://root:123456@192.168.1.45:27017/'

ENTRYPOINT uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
