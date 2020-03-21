from zope.annotation.interfaces import IAttributeAnnotatable

from zope.container.interfaces import IContainer
from zope.location.interfaces import IContained

from zope.schema import Choice
from zope.schema import Number
from zope.schema import Object
from zope.schema import Text
from zope.schema import TextLine

from testme.models.interfaces import IUser

PROJECT_TYPES = ('Software', )


class IJiraContainer(IContainer):
    """
    The root container for all jira objects.
    """


class IProjectContainer(IContainer):
    """
    An object capable of storing all projects, keyed by project_name.
    """


class IProject(IContained):

    project_name = TextLine(title="The name of the project.")

    project_type = Choice(PROJECT_TYPES,
                          title="The type of this project.",
                          required=True)

    project_lead = Object(IUser,
                          title="Who leads this project.",
                          required=True)


class ITicketContainer(IContainer):
    """
    An object capable of storing tickets, keyed by ticket_name.
    """


class ITicket(IContained, IAttributeAnnotatable):

    ticket_name = TextLine(title="The name of the ticket.",
                           description="Globally unique, used as key.",
                           required=True)

    title = TextLine(title="The title of the ticket.",
                     description="Briefly summarize the ticket.",
                     required=True)

    description = Text(title="The details about the ticket.",
                       required=False)

    project = Object(IProject,
                     title="The project this ticket belongs to.",
                     required=True)


class ITicketCommentsContainer(IContainer):
    """
    Keyed by comment id.
    """


class ITicketComment(IContained):

    creator = Object(IUser,
                     title="The creator",
                     required=True)

    description = Text(title="The details.",
                       required=True)

    createdTime = Number(title="The utc timestamp.",
                         required=True)
