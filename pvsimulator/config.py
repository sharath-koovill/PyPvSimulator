"""
PV Simulator global variables
"""
import os
from pathlib import Path

BROKER_ADDRESS = "amqp://guest:guest@127.0.0.1/"
EXCHANGE_NAME = "pv_simulator_exchange"
QUEUE_NAME = "pv_simulator_queue"
PV_MIN = 0
PV_MAX = 4000
CONSUMER_TIME_INTERVAL = 10
CSV_FOLDER = os.path.join(str(Path(__file__).resolve().parents[1]),  "csv_storage")
CSV_FIELDS = ['timestamp', 'meter_power_value', 'PV_power_value', 'sum_of_powers']
LOG_DIRECTORY = os.path.join(str(Path(__file__).resolve().parents[1]),  "log")
LOG_NAME = "pv_simulator.log"
