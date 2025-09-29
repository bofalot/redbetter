FROM python:3.9.21-slim

RUN set -x \
  && apt-get update \
  && apt-get install -y musl lame sox flac mktorrent \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD requirements.txt /app

RUN set -x && pip install -r requirements.txt

ADD redbetter/* /app

USER nobody

EXPOSE 9725
