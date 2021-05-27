"""
Settings is used for defining global variables
"""
import os
from pathlib import Path

BROKER_ADDRESS = "amqp://guest:guest@127.0.0.1/"
EXCHANGE_NAME = "pv_simulator_exchange"
QUEUE_NAME = "pv_simulator_queue"
PV_MIN = 0
PV_MAX = 9000
PRODUCER_TIME_INTERVAL = 10
LOG_DIRECTORY = os.path.join(str(Path(__file__).resolve().parents[1]),  "log")
LOG_NAME = "meter.log"


