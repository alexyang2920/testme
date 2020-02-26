from zope import component
from zope import interface

from zope.annotation.interfaces import IAnnotations

from testme.models.interfaces import IUser

from testme.chat.interfaces import IMailbox
from testme.chat.message import Mailbox


MAILBOX_ANNOTATION_KEY = 'mailbox'


@component.adapter(IUser)
@interface.implementer(IMailbox)
def get_mailbox(user, create=True):
    result = None
    annotations = IAnnotations(user)
    try:
        result = annotations[MAILBOX_ANNOTATION_KEY]
    except KeyError:
        if create:
            result = Mailbox(owner=user)
            annotations[MAILBOX_ANNOTATION_KEY] = result
            result.__name__ = MAILBOX_ANNOTATION_KEY
            result.__parent__ = user
    return result
