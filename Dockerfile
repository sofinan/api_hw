FROM ubuntu:latest
RUN apt update -y
RUN apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools git -y
RUN pip install uwsgi flask pymongo requests

RUN mkdir app
RUN git clone https://github.com/sofinan/api_hw.git
WORKDIR api_hw

ENTRYPOINT ["python3","app.py"]
