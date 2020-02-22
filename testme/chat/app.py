import json

from geventwebsocket import WebSocketApplication

logger = __import__('logging').getLogger(__name__)


class ChatApplication(WebSocketApplication):

    def on_open(self):
        logger.info("Some client connected!")

    def on_message(self, message):
        if message is None:
            return

        message = json.loads(message)

        if message['msg_type'] == 'message':
            self.broadcast(message)
        elif message['msg_type'] == 'update_clients':
            self.send_client_list(message)

    def send_client_list(self, message):
        current_client = self.ws.handler.active_client
        current_client.username = message['username']

        self.ws.send(json.dumps({
            'msg_type': 'update_clients',
            'clients': [
                getattr(client, 'username', 'anonymous')
                for client in self.ws.handler.server.clients.values()
            ]
        }))

    def broadcast(self, message):
        for client in self.ws.handler.server.clients.values():
            client.ws.send(json.dumps({
                'msg_type': 'message',
                'username': message['username'],
                'message': message['message']
            }))

    def on_close(self, reason):
        logger.info("Connection closed!")


def create_chat_app(**settings):
    return ChatApplication
