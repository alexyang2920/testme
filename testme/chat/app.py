import json
import gevent
import transaction

from geventwebsocket import WebSocketApplication

from ZODB.interfaces import IDatabase

from zope import component

from zope.component.hooks import site as set_site

from zope.cachedescriptors.property import Lazy

from testme.redis import IRedisClient

from testme.chat.utils import store_data
from testme.chat.utils import fetch_messages

logger = __import__('logging').getLogger(__name__)


_USERS_MSG_CHANNEL = '/users/messages'


class ChatApplication(WebSocketApplication):

    def __init__(self, ws):
        super(ChatApplication, self).__init__(ws)
        self._init()

    def _init(self):
        if not getattr(self.server, '_connections_to_users', None):
            self.server._connections_to_users = dict()

        if not getattr(self.server, '_users_to_connections', None):
            self.server._users_to_connections = dict()

        if not getattr(self.server, '_redis_job_spawned', False):
            self.server._redis_job_spawned = True
            spawn_redis_job(self.server)

    @property
    def server(self):
        return self.ws.handler.server

    @Lazy
    def redis(self):
        return component.getUtility(IRedisClient)._cli

    def on_open(self):
        logger.info("Some client connected!")

    def on_message(self, message):
        if message is None:
            return

        message = json.loads(message)
        if message['msg_type'] == 'ping':
            self.pong()
        elif message['msg_type'] == 'auth':
            self.auth(message)
        elif message['msg_type'] == 'message':
            # format: 
            # {"msg_type": "message", "username": "sender", "target": "receiver", "message": "Hello sender"}
            self.redis.publish(_USERS_MSG_CHANNEL, json.dumps(message))

    def auth(self, message):
        """
        After a connection opened, server expected a auth message from server.
        or maybe server should send something to client, then get this message, and auth it.
        """
        username = message['username']

        if username in self.server._users_to_connections:
            cli = self.server._users_to_connections[username]
            if not cli.ws.closed:
                cli.ws.close()

            del self.server._connections_to_users[cli];
            del self.server._users_to_connections[username]
            logger.info("Old connection closed: %s.", username)

        self.server._users_to_connections[username] = cli = self.ws.handler.active_client
        self.server._connections_to_users[cli] = username

        cli.ws.send(json.dumps({
            'msg_type': 'authed',
            'username': username
        }))

        logger.info("%s authed.", username)

        messages = get_messages(username)
        for msg in messages or ():
            cli.ws.send(json.dumps(msg))

    def pong(self):
        cli = self.ws.handler.active_client
        cli.ws.send(json.dumps({'msg_type': 'pong'}))

    def on_close(self, reason):
        pass


def create_chat_app(**settings):
    return ChatApplication


def spawn_redis_job(server):
    cli = component.getUtility(IRedisClient)._cli
    pubsub=cli.pubsub()
    pubsub.subscribe(_USERS_MSG_CHANNEL)
    
    db = component.getUtility(IDatabase)
    def _do_job():
        # FIXME: add fine transaction handling.
        try:
            site = db.open().root()['Application']['testme']
            with set_site(site):
                for msg in pubsub.listen():
                    if msg and msg['type'] == 'message':
                        data = json.loads(msg['data'])
                        send_messages(server, data)
                        transaction.commit()
        except:
            transaction.abort()

    gevent.spawn(_do_job)


def send_messages(server, data):
    # for off-line target users
    # we may need to store somewhere,
    # and load them once the user login.
    target = data['target']
    if target == 'users':
        logger.info("A new message sending to all users.")
        for client in server.clients.values():
            client.ws.send(json.dumps(data))
    else:
        logger.info("A new message sending to user: %s.", target)
        client = server._users_to_connections.get(target)
        if client and not client.ws.closed:
            client.ws.send(json.dumps(data))

        # persistent
        store_data(data)

def get_messages(username):
    db = component.getUtility(IDatabase)
    site = db.open().root()['Application']['testme']
    with set_site(site):
        return fetch_messages(username)
