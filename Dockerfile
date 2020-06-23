# FROM python:3.7
# #-alpine
# ENV FLASK_APP app.py
# ENV FLASK_RUN_HOST 0.0.0.0
# WORKDIR /data/www
# # RUN sh -c "apk add gcc python3-dev musl-dev postgresql-dev libpq"  
# #--virtual .build-deps
# RUN sh -c "apt update && apt install gcc python3-dev musl-dev  libpq-dev -y"  
# #postgresql-dev
# # RUN sh -c "apk add postgresql-libs"
# #RUN sh -c "apt install postgresql-libs"
# COPY requirements.txt requirements.txt
# RUN sh -c "pip install -r requirements.txt "
# # RUN sh -c "apk del .build-deps"
# # COPY . .
# # CMD sh -c "gunicorn --bind=flask:3000 --workers=4 app:app"


# https://www.rockyourcode.com/install-psycopg2-binary-with-docker/
## base image
FROM python:3.7-alpine

## install dependencies
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## set working directory
WORKDIR /data/www

## add user
# RUN adduser -D user
# RUN chown -R user:user /usr/src/app && chmod -R 755 /usr/src/app

## add and install requirements
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apk del build-deps
## add entrypoint.sh
# COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
# RUN chmod +x /usr/src/app/entrypoint.sh

## switch to non-root user
# USER user

## add app
# COPY . /usr/src/app

## run server
# CMD python manage.py run -h 0.0.0.0
