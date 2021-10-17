FROM python:3.8-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY misc.py .
COPY nightscout.py .
COPY config.yml .

ENV FLASH_APP=app

EXPOSE 5000

CMD python run.py
