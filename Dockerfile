FROM python:3.12-alpine3.19

COPY requirements.txt /temp/requirements.txt

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

COPY web /web
WORKDIR /web
EXPOSE 8000

RUN adduser --disabled-password service-user
USER service-user