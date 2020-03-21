from zope import component
from zope import interface

from zope.annotation.interfaces import IAnnotations

from testme.jira.interfaces import ITicket, ITicketCommentsContainer
from testme.jira.model import TicketCommentsContainer


TICKET_COMMENTS_ANNOTATION_KEY = 'comments'


@interface.implementer(ITicketCommentsContainer)
@component.adapter(ITicket)
def _ticket_comments_factory(ticket, create=True):
    result = None
    annotations = IAnnotations(ticket)
    try:
        result = annotations[TICKET_COMMENTS_ANNOTATION_KEY]
    except KeyError:
        if create:
            result = TicketCommentsContainer()
            annotations[TICKET_COMMENTS_ANNOTATION_KEY] = result
            result.__name__ = TICKET_COMMENTS_ANNOTATION_KEY
            result.__parent__ = ticket
    return result
