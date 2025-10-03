# Frontend build stage
FROM node:18 AS builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Final stage
FROM python:3.9-slim

RUN set -x \
  && apt-get update \
  && apt-get install -y musl lame sox flac mktorrent \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/frontend/build ./frontend/build
COPY requirements.txt .

RUN set -x && pip install -r requirements.txt

COPY . .

RUN flake8 redbetter tests
ENV PYTHONPATH=/app
RUN pytest

USER nobody

EXPOSE 9725