"""
This will orchestrate the meter to connect to
the broker and pass the power values to the broker
"""

import sys
import os
import time
import logger
import pv_simulator
import config as cfg
from aio_pika.exceptions import AMQPConnectionError
from broker_client import BrokerClient
from consumer import Consumer

simulator_log = logger.setup_logging("pv_simulator")


async def consume() -> None:
    broker_address = cfg.BROKER_ADDRESS
    broker_exchange_name = cfg.EXCHANGE_NAME
    broker_queue_name = cfg.QUEUE_NAME

    broker_client = BrokerClient(broker_address, broker_exchange_name, broker_queue_name)
    simulator_log.info("Created Broker Client using address %s, exchange %s, queue %s"
                       % (broker_address, broker_exchange_name, broker_queue_name))

    # Initialize the broker to the consumer
    consumer = Consumer(broker_client)
    try:
        # Connect to the broker using the broker client
        await consumer.connect_to_broker()

        while True:
            simulator_log.info("Sleeping for %d seconds" % cfg.CONSUMER_TIME_INTERVAL)
            # Consume messages after every CONSUMER_TIME_INTERVAL
            time.sleep(cfg.CONSUMER_TIME_INTERVAL)
            simulator_log.info("Receiving message from broker")
            # Consume the message from the broker
            await consumer.consume(pv_simulator.process_message)

    except KeyboardInterrupt:
        simulator_log.info("key board interrupted, Exiting the program")
    except AMQPConnectionError as e:
        simulator_log.error(e)
    except Exception as e:
        simulator_log.error(e)

    finally:
        simulator_log.info("Orchestrator disconnecting from the consumer")
        await consumer.disconnect_from_broker()
        simulator_log.info("Finished: Orchestrator disconnected from the consumer")
        sys.exit(0)

