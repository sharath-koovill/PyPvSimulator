import unittest
import asyncio
import config as cfg
from meter import Meter


class TestMeter(unittest.TestCase):
    def test_generate_power_value(self):
        meter_house_a = Meter("HOUSE_A")
        loop = asyncio.get_event_loop()
        power_value = loop.run_until_complete(meter_house_a.generate_power_value())

        self.assertTrue(power_value["house"] is "HOUSE_A")
        self.assertIsInstance(power_value["house"], str)
        self.assertIsInstance(power_value["datetime"], float)
        self.assertIsInstance(power_value["pv"], int)
        self.assertTrue(cfg.PV_MIN < power_value["pv"] < cfg.PV_MAX)


if __name__ == "__main__":
    unittest.main()
