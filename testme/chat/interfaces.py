from zope import interface
from zope.container.interfaces import IContainer
from zope.container.constraints import contains

from zope.schema import Object
from zope.schema import Float
from zope.schema import Text

from testme.models.interfaces import IUser


class IMessage(interface.Interface):

    sender = Object(IUser,
                    title="sender",
                    required=True)

    receiver = Object(IUser,
                      title="receiver",
                      required=True)

    message = Text(title="The content",
                   required=True)

    last_viewed = Float(title="The time this message is viewed by receiver.",
                        required=False)


class IMessageContainer(IContainer):
    """
    An object capable of storing all messages that
    a user sent to another user.
    """
    contains(IMessage)


class IMailbox(IContainer):
    """
    Store all messages a user sent. keyed by receiver.
    """
    owner = Object(IUser,
                   title="The user who owner this container.",
                   required=True)

    contains(IMessageContainer)
