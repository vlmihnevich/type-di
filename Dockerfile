FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY . . 

RUN pip install --no-cache-dir -r conf/requirements.txt
