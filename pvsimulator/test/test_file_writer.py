import os
import unittest
import asyncio
import datetime
import csv
import config as cfg
import file_writer


class TestFileWriter(unittest.TestCase):
    def setUp(self):
        self._loop = asyncio.get_event_loop()
        self._house = "HOUSE_TEST"
        self._timestamp = datetime.datetime.now().timestamp()
        self._meter_power_value = 1200
        self._pv_power_value = 1300
        self._file_path = self._loop.run_until_complete(
            file_writer.generate_filepath(self._house, self._timestamp))

    def tearDown(self):
        if os.path.isfile(self._file_path):
            os.remove(self._file_path)

    def test_write_and_csv_file_content(self):
        data = {"timestamp": self._timestamp,
                "meter_power_value": self._meter_power_value,
                "PV_power_value": self._pv_power_value,
                "sum_of_powers": self._meter_power_value + self._pv_power_value}
        try:
            self._loop.run_until_complete(file_writer.write(self._file_path, data))
            self.assertTrue(os.path.isfile(self._file_path))
            with open(self._file_path, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file)
                field_names = next(csv_reader)
                self.assertTrue(field_names == cfg.CSV_FIELDS)
        except FileNotFoundError as e:
            self.assertTrue(False, msg=e)
