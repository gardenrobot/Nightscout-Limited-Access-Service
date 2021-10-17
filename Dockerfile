FROM python:3.8-slim

RUN mkdir /nlas
WORKDIR /nlas

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.py .
COPY config.py .
COPY app ./app

ENV FLASH_APP=app

EXPOSE 5000

CMD python run.py
