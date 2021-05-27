import unittest
import asyncio
import config as cfg
import pv_simulator
from broker_client import BrokerClient


class TestBrokerClient(unittest.TestCase):
    def test_connect(self):
        broker_address = cfg.BROKER_ADDRESS
        broker_exchange_name = cfg.EXCHANGE_NAME
        broker_queue_name = cfg.QUEUE_NAME
        broker_client = BrokerClient(broker_address, broker_exchange_name, broker_queue_name)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(broker_client.connect())

        self.assertIsInstance(broker_client, BrokerClient)
        self.assertTrue(broker_client)

    def test_get(self):
        broker_address = cfg.BROKER_ADDRESS
        broker_exchange_name = cfg.EXCHANGE_NAME
        broker_queue_name = cfg.QUEUE_NAME
        broker_client = BrokerClient(broker_address, broker_exchange_name, broker_queue_name)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(broker_client.connect())
        loop.run_until_complete(broker_client.get(pv_simulator.process_message))

        self.assertIsInstance(broker_client, BrokerClient)
        self.assertTrue(broker_client)

    def test_close_connection(self):
        broker_address = cfg.BROKER_ADDRESS
        broker_exchange_name = cfg.EXCHANGE_NAME
        broker_queue_name = cfg.QUEUE_NAME
        broker_client = BrokerClient(broker_address, broker_exchange_name, broker_queue_name)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(broker_client.connect())
        loop.run_until_complete(broker_client.close_connection())

        self.assertIsInstance(broker_client, BrokerClient)
        self.assertTrue(broker_client)


if __name__ == "__main__":
    unittest.main()