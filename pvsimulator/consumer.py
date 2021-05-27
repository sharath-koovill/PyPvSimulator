
class Consumer:
    """
    Consumer class for connecting, consuming the message
        and finally closing the connection
    """

    def __init__(self, broker_client):
        self._broker_client = broker_client

    async def connect_to_broker(self):
        await self._broker_client.connect()

    async def consume(self, callback):
        await self._broker_client.get(callback)

    async def disconnect_from_broker(self):
        await self._broker_client.close_connection()
