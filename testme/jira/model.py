from zope import interface

from zope.container.folder import Folder
from zope.container.contained import Contained

from zope.schema.fieldproperty import createFieldProperties

from persistent import Persistent

from testme.jira.interfaces import IJiraContainer, IProject, IProjectContainer,\
    ITicketContainer, ITicket, ITicketCommentsContainer, ITicketComment

from testme.models.base import Base


@interface.implementer(IJiraContainer)
class JiraContainer(Folder):
    pass


@interface.implementer(IProjectContainer)
class ProjectContainer(Folder):

    def store_project(self, proj):
        self[proj.project_name] = proj
        return proj


@interface.implementer(IProject)
class Project(Base, Persistent, Contained):

    createFieldProperties(IProject)

    def __init__(self, project_name, project_type, project_lead):
        self.project_name = project_name
        self.project_type = project_type
        self.project_lead = project_lead


@interface.implementer(ITicketContainer)
class TicketContainer(Folder):

    def store_ticket(self, ticket):
        self[ticket.ticket_name] = ticket
        return ticket


@interface.implementer(ITicket)
class Ticket(Base, Persistent, Contained):

    createFieldProperties(ITicket)


@interface.implementer(ITicketCommentsContainer)
class TicketCommentsContainer(Folder):

    _next_id = 0

    def _generate_id(self):
        self._next_id += 1
        while str(self._next_id) in self:
            self._next_id += 1
        return self._next_id

    def store_comment(self, comment):
        comment.id = self._generate_id()
        self[comment.id] = comment
        return comment


@interface.implementer(ITicketComment)
class TicketComment(Base, Persistent, Contained):

    createFieldProperties(ITicketComment)
