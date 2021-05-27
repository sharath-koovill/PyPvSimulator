FROM python:3.9-alpine

WORKDIR /usr/src/pv_simulator

COPY __init__.py .
COPY __main__.py .
COPY orchestrator.py .
COPY consumer.py .
COPY pv_simulator.py .
COPY broker_client.py .
COPY config.py .
COPY logger.py .
COPY file_writer.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "__main__.py" ]