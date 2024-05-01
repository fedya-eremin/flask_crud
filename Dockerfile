FROM python:3.10.13

WORKDIR /flask_crud

COPY src src
COPY requirements.txt .

RUN pip install -r requirements.txt
