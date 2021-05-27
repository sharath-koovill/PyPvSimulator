import unittest
import asyncio
import config as cfg
import pv_simulator
from consumer import Consumer
from broker_client import BrokerClient


class TestConsumer(unittest.TestCase):
    def setUp(self):
        broker_address = cfg.BROKER_ADDRESS
        broker_exchange_name = cfg.EXCHANGE_NAME
        broker_queue_name = cfg.QUEUE_NAME
        broker_client_obj = BrokerClient(broker_address, broker_exchange_name, broker_queue_name)
        self._consumer = Consumer(broker_client_obj)

    def test_connect_to_broker(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._consumer.connect_to_broker())
            self.assertTrue(True)
        except ConnectionError:
            self.assertTrue(False)

    def test_consume(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._consumer.connect_to_broker())
            loop.run_until_complete(self._consumer.consume(pv_simulator.process_message))
            self.assertTrue(True)
        except ConnectionError:
            self.assertTrue(False)

    def test_disconnect_from_broker(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._consumer.connect_to_broker())
            loop.run_until_complete(self._consumer.disconnect_from_broker())
            self.assertTrue(True)
        except ConnectionError:
            self.assertTrue(False)
