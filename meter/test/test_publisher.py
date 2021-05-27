import unittest
import asyncio
import config as cfg

from publisher import Publisher
from broker_client import BrokerClient
from meter import Meter


class TestPublisher(unittest.TestCase):
    def setUp(self):
        broker_address = cfg.BROKER_ADDRESS
        broker_exchange_name = cfg.EXCHANGE_NAME
        broker_queue_name = cfg.QUEUE_NAME
        broker_client_obj = BrokerClient(broker_address, broker_exchange_name, broker_queue_name)
        self._publisher = Publisher(broker_client_obj)

    def test_connect_to_broker(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._publisher.connect_to_broker())
            self.assertTrue(True)
        except ConnectionError:
            self.assertTrue(False)

    def test_publish(self):
        try:
            meter_house = Meter("HOUSE_TEST")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._publisher.connect_to_broker())
            pv_house_a = loop.run_until_complete(meter_house.generate_power_value())
            loop.run_until_complete(self._publisher.publish(pv_house_a))
            self.assertTrue(True)
        except ConnectionError:
            self.assertTrue(False)

    def test_disconnect_from_broker(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._publisher.connect_to_broker())
            loop.run_until_complete(self._publisher.disconnect_from_broker())
            self.assertTrue(True)
        except ConnectionError:
            self.assertTrue(False)
