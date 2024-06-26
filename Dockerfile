FROM python:3.9-alpine
LABEL maintainer="marketafajtova.com"

COPY ./requirements.txt /requirements.txt
COPY ./Portfolio /Portfolio
WORKDIR /Portfolio

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user