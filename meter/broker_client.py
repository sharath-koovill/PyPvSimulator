"""
Broker is used as a wrapper for sending messages to the broker(RabbitMQ)
and to connect/disconnect to broker
"""

import json
import logger
from aio_pika import connect, ExchangeType, Message

meter_log = logger.setup_logging("meter")


class BrokerClient:
    _connection = object
    _channel = object
    _exchange = object
    _broker_queue = object

    def __init__(self, address: str, exchange_name: str, queue_name: str):
        self._address = address
        self._exchange_name = exchange_name
        self._queue_name = queue_name

    async def connect(self):
        meter_log.info("BrokerClient connecting to RabbitMQ %s" % self._address)
        self._connection = await connect(self._address)
        meter_log.info("Connected to RabbitMQ %s" % self._address)

        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            self._exchange_name,
            type=ExchangeType.DIRECT,
            durable=True,
        )
        meter_log.info("BrokerClient finished declaring exchange %s" % self._exchange_name)

        self._broker_queue = await self._channel.declare_queue(
            self._queue_name,
            durable=True,
            arguments={"x-queue-type": "quorum",
                       # "x-message-ttl": 60000,
                       "x-dead-letter-exchange": self._exchange.name
                       }
        )
        meter_log.info("BrokerClient finished declaring queue %s" % self._queue_name)

        await self._broker_queue.bind(self._exchange)
        meter_log.info("Queue %s finished binding to exchange %s"
                       % (self._queue_name, self._exchange.name))

    async def put(self, message: dict):
        message_json = json.dumps(message)
        await self._channel.default_exchange.publish(
            Message(message_json.encode('utf-8')),
            routing_key=self._queue_name
        )
        meter_log.info("BrokerClient publishing message %s to Queue %s"
                       % (message_json, self._queue_name))

    async def close_connection(self):
        await self._connection.close()
        meter_log.info("BrokerClient closed connection with RabbitMQ")
