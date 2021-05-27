"""
Broker client is used as a wrapper for receiving messages sent by the producer(meter)
and to connect/disconnect to the rabbitmq queue
"""
import logger
from aio_pika import connect, ExchangeType

simulator_log = logger.setup_logging("pv_simulator")


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
        simulator_log.info("BrokerClient connecting to RabbitMQ %s" % self._address)
        self._connection = await connect(self._address)
        simulator_log.info("Connected to RabbitMQ %s" % self._address)

        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            self._exchange_name,
            type=ExchangeType.DIRECT,
            durable=True,
        )
        simulator_log.info("BrokerClient finished declaring exchange %s" % self._exchange_name)

        self._broker_queue = await self._channel.declare_queue(
            self._queue_name,
            durable=True,
            arguments={"x-queue-type": "quorum",
                       "x-dead-letter-exchange": self._exchange.name
                       }
        )
        simulator_log.info("BrokerClient finished declaring queue %s" % self._queue_name)

        await self._broker_queue.bind(self._exchange)
        simulator_log.info("Queue %s finished binding to exchange %s"
                       % (self._queue_name, self._exchange.name))

    async def get(self, callback):
        await self._broker_queue.consume(callback, no_ack=True)
        simulator_log.info("BrokerClient consuming messages from Queue %s" % self._queue_name)

    async def close_connection(self):
        await self._connection.close()
        simulator_log.info("BrokerClient closed connection with RabbitMQ")
