FROM python:3.6-alpine

LABEL maintainer "Stephan Cilliers <stephanus.cilliers@gmail.com>"

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile
