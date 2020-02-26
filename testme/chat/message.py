from persistent import Persistent

from zope import interface

from zope.container.contained import Contained

from zope.container.folder import Folder

from zope.schema.fieldproperty import createFieldProperties

from testme.chat.interfaces import IMailbox
from testme.chat.interfaces import IMessage
from testme.chat.interfaces import IMessageContainer

from testme.models.base import Base


@interface.implementer(IMessage)
class Message(Base, Persistent, Contained):

    createFieldProperties(IMessage)

    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message


@interface.implementer(IMessageContainer)
class MessageContainer(Folder):

    _cur_id = 0

    def _generate_key(self):
        self._cur_id += 1
        while str(self._cur_id) in self:
            self._cur_id += 1
        return str(self._cur_id)

    def store_message(self, message):
        key = self._generate_key()
        self[key] = message
        return message


@interface.implementer(IMailbox)
class Mailbox(Folder):

    def __init__(self, owner):
        super(Mailbox, self).__init__()
        self.owner = owner

    def store_message(self, message):
        key = message.receiver.username
        folder = self.get(key)
        if folder is None:
            folder = self[key] = MessageContainer()
        return folder.store_message(message)
