FROM python:3.11-alpine

RUN python3 -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .