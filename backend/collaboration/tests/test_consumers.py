from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from backend.config.asgi import application
import json

class DocumentConsumerTests(TransactionTestCase):
    async def test_document_connection_and_echo(self):
        communicator = WebsocketCommunicator(application, "ws/doc/testroom/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        # Send a message
        payload = {'content': 'Hello, World!'}
        await communicator.send_to(text_data=json.dumps(payload))

        # Receive the broadcast
        response = await communicator.receive_from()
        response_data = json.loads(response)
        self.assertEqual(response_data['content'], 'Hello, World!')

        await communicator.disconnect()
