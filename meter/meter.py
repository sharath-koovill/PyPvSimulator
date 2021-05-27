"""
Meter class is used as a producer to generate
the random continuous power values
"""

import datetime
import random
import logger
import config as cfg

meter_log = logger.setup_logging("meter")


class Meter:
    """
    This class will generate PV for a given house with current timestamp
    """
    def __init__(self, house: str):
        self._house = house

    async def generate_power_value(self) -> dict:
        """
        producer will generate a random value between 0 to 9000
        """
        today_datetime = datetime.datetime.now().timestamp()
        pv = random.randint(cfg.PV_MIN, cfg.PV_MAX+1)
        meter_log.info("Meter generating power value %s with timestamp %d for house %s"
                       % (pv, today_datetime, self._house))
        return {"house": self._house,
                "datetime": today_datetime,
                "pv": pv}


