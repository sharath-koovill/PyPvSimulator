import os
import unittest
import asyncio
import datetime
import json
import pv_simulator
import config as cfg
import file_writer
from unittest.mock import Mock


class TestPVSimulator(unittest.TestCase):
    def setUp(self):
        self._loop = asyncio.get_event_loop()

    def test_generate_simulator_power_value(self):
        power_value = self._loop.run_until_complete(pv_simulator.generate_simulator_power_value())

        self.assertIsInstance(power_value, int)
        self.assertTrue(cfg.PV_MIN < power_value < cfg.PV_MAX)

    def test_add_power_value(self):
        meter_pv = 1000
        power_value = self._loop.run_until_complete(pv_simulator.generate_simulator_power_value())
        sum_power_value = self._loop.run_until_complete(pv_simulator.add_power_value(meter_pv, power_value))

        self.assertIsInstance(sum_power_value, int)

    @staticmethod
    def writer_mock(file_path: str, data: dict):
        fw_mock = Mock()
        fw_mock.write.return_value = None
        return fw_mock

    def test_process_message(self):
        message = Mock()
        body = {"house": "HOUSE_TEST",
                "datetime": datetime.datetime.now().timestamp(),
                "pv": 1200}
        message.body = body
        message.body = json.dumps(message.body)
        message.body = message.body.encode('utf-8')

        fw = Mock()
        fw.write.side_effect = self.writer_mock
        try:
            self._loop.run_until_complete(pv_simulator.process_message(message))
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)
        finally:
            file_path = self._loop.run_until_complete(
                file_writer.generate_filepath(body["house"], body["datetime"]))
            if os.path.isfile(file_path):
                os.remove(file_path)


if __name__ == "__main__":
    unittest.main()
