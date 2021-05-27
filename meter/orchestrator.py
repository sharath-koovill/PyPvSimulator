"""
This will orchestrate the producer to connect to
the broker and pass the power values to the broker
"""

import sys
import time
import meter
import config as cfg
import logger
from aio_pika.exceptions import AMQPConnectionError
from broker_client import BrokerClient
from publisher import Publisher

meter_log = logger.setup_logging("meter")


async def produce() -> None:
    broker_address = cfg.BROKER_ADDRESS
    broker_exchange_name = cfg.EXCHANGE_NAME
    broker_queue_name = cfg.QUEUE_NAME

    # Creating a broker client to connect to RabbitMQ
    broker_client = BrokerClient(broker_address, broker_exchange_name, broker_queue_name)
    meter_log.info("Created Broker Client using address %s, exchange %s, queue %s"
                   % (broker_address, broker_exchange_name, broker_queue_name))

    # Creating meters mocking few houses in a neighbourhood
    meter_house_a = meter.Meter("HOUSE_A")
    meter_house_b = meter.Meter("HOUSE_B")
    meter_house_c = meter.Meter("HOUSE_C")

    # Publisher which publishes the message to the RabbitMQ queue
    publisher = Publisher(broker_client)
    try:
        # Connect to the broker using the broker client
        await publisher.connect_to_broker()

        # publish messages after every PRODUCER_TIME_INTERVAL
        while True:
            meter_log.info("Sleeping for %d seconds" % cfg.PRODUCER_TIME_INTERVAL)
            time.sleep(cfg.PRODUCER_TIME_INTERVAL)
            pv_house_a = await meter_house_a.generate_power_value()
            meter_log.info("Sending message to broker from house meter HOUSE_A")
            await publisher.publish(pv_house_a)

            meter_log.info("Sleeping for %d seconds" % cfg.PRODUCER_TIME_INTERVAL)
            time.sleep(cfg.PRODUCER_TIME_INTERVAL)
            pv_house_b = await meter_house_b.generate_power_value()
            meter_log.info("Sending message to broker from house meter HOUSE_B")
            await publisher.publish(pv_house_b)

            meter_log.info("Sleeping for %d seconds" % cfg.PRODUCER_TIME_INTERVAL)
            time.sleep(cfg.PRODUCER_TIME_INTERVAL)
            pv_house_c = await meter_house_c.generate_power_value()
            meter_log.info("Sending message to broker from house meter HOUSE_C")
            await publisher.publish(pv_house_c)

    except KeyboardInterrupt:
        meter_log.info("key board interrupted, Exiting the program")
    except AMQPConnectionError as e:
        meter_log.error(e)
    except Exception as e:
        meter_log.error(e)

    finally:
        meter_log.info("Orchestrator disconnecting from the publisher")
        await publisher.disconnect_from_broker()
        meter_log.info("Finished: Orchestrator disconnected from the publisher")
        sys.exit(0)