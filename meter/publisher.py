
class Publisher:
    """
    Publisher class for connecting, publishing the message
    and finally closing the connection
    """

    def __init__(self, broker_client):
        self._broker_client = broker_client

    async def connect_to_broker(self):
        await self._broker_client.connect()

    async def publish(self, message: dict):
        await self._broker_client.put(message)

    async def disconnect_from_broker(self):
        await self._broker_client.close_connection()
