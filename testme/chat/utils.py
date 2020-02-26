from zope import component

from testme.chat.interfaces import IMailbox
from testme.chat.message import Message

from testme.models.interfaces import IUsersFolderFactory

logger = __import__('logging').getLogger(__name__)


def store_data(data, sender=None):
    """
    data format: 
    { "message": "Hello", "username": "alex", "target": "moggy" }
    """
    users = component.getUtility(IUsersFolderFactory)()
    if sender is None:
        sender = users.getUser(data['username'])

    if sender is None:
        return

    receiver = users.getUser(data['target'])
    if receiver is None:
        return

    msg = Message(sender=sender,
                  receiver=receiver,
                  message=data['message'])

    logger.info("persistent msg sent by %s.", sender.username)
    mailbox = IMailbox(sender)
    return mailbox.store_message(msg)


def fetch_messages(username):
    result = []
    users = component.getUtility(IUsersFolderFactory)()
    for user in users.values():
        mailbox = IMailbox(user)
        msgs = mailbox.get(username)
        if msgs is None:
            continue
        for msg in msgs.values() or ():
            result.append({'msg_type': 'message',
                           'username': msg.sender.username,
                           'target': username,
                           'message': msg.message})
    return result
