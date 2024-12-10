FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN mkdir -p /app/bin
COPY bin/chromedriver ./bin/chromedriver
RUN pip install --no-cache-dir -r requirements.txt
