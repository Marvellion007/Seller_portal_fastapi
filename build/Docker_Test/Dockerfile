FROM python:3

ARG ports

ENV port=$ports

COPY ./build/Docker_Test/requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /code

COPY ./test .

COPY ./core ./core

RUN python3 test.py $ports

