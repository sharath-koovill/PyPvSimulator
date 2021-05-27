"""
This will write the timestamp, meter power value, PV power value, sum of the powers to a CSV file.
"""

import csv
import os.path
import config as cfg
import logger
from datetime import datetime

simulator_log = logger.setup_logging("pv_simulator")


async def write(file_path: str, data: dict) -> None:
    """
    :param file_path: path to the file
    :param data: data with fields ['timestamp', 'meter_power_value', 'PV_power_value', 'sum_of_powers']
    :return: None
    """
    simulator_log.info("File writer requested for filepath %s" % file_path)
    new_file = True
    if os.path.isfile(file_path):
        new_file = False
    with open(file_path, mode='a+', newline='') as csv_file:
        fieldnames = cfg.CSV_FIELDS
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if new_file:
            writer.writeheader()
        writer.writerow(data)
        simulator_log.info("File writer finished writing to file path %s" % file_path)



async def generate_filepath(house_name: str, time_stamp: int) -> str:
    """
    :param house_name:
    :param time_stamp:
    :return: Combines house name and date in %Y%m%d format
    """
    date = datetime.utcfromtimestamp(time_stamp).strftime('%Y%m%d')
    return os.path.join(cfg.CSV_FOLDER, house_name + "_" + date + ".csv")