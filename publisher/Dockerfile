FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install paho-mqtt flask

CMD ["python", "publisher.py"]
