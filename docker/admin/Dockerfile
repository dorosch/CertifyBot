FROM python:3.10-alpine

ENV PATH="${PATH}:/usr/local/lib/python3.10/site-packages"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip3 install --no-cache-dir poetry==1.8.2 && \
    poetry config virtualenvs.create false

RUN poetry install --no-root --no-interaction --extras admin

COPY service/ .
