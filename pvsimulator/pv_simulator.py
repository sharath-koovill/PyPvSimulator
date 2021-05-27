"""
PV Simulator class is used to generate the power value
from a Photovoltaic cell with assumption that it
generates a value from 0 to 4000 Watts
"""

import random
import logger
import json
import config as cfg
import file_writer as fw
from aio_pika import IncomingMessage

simulator_log = logger.setup_logging("pv_simulator")


async def generate_simulator_power_value() -> int:
    """
    producer will generate a random value between 0 to 4000 watts
    """
    power_value = random.randint(cfg.PV_MIN, cfg.PV_MAX + 1)
    simulator_log.info("Generating PV simulator power value %d" % power_value)
    return power_value


async def add_power_value(meter_pv: int, simulator_pv: int) -> int:
    """
    :param meter_pv:
    :param simulator_pv:
    :return: Sum of meter_pv and simulator_pv
    """
    return meter_pv + simulator_pv


async def process_message(message: IncomingMessage):
    meter_message = json.loads(message.body.decode('utf-8'))
    simulator_log.info("Incoming message from the Queue %s" % meter_message)

    filepath = await fw.generate_filepath(meter_message["house"], meter_message["datetime"])
    pv_simulator_power_value = await generate_simulator_power_value()
    sum_power_value = await add_power_value(meter_message["pv"], pv_simulator_power_value)
    data = {"timestamp": meter_message["datetime"],
            "meter_power_value": meter_message["pv"],
            "PV_power_value": pv_simulator_power_value,
            "sum_of_powers": sum_power_value}

    simulator_log.info("Final data produced from the PV simulator %s" % str(data))
    await fw.write(filepath, data)
