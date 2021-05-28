FROM python:3.9-slim-buster

WORKDIR /usr/src/meter

COPY __init__.py .
COPY __main__.py .
COPY orchestrator.py .
COPY meter.py .
COPY publisher.py .
COPY broker_client.py .
COPY config.py .
COPY logger.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "__main__.py" ]