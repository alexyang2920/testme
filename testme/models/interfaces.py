
from zope.container.interfaces import IContainer
from zope.container.constraints import contains
from zope.location.interfaces import IContained

from zope.schema import TextLine


class IApplicationRoot(IContainer):
    pass


class IUser(IContained):

    username = TextLine(title="The username",
                        required=True)

    password = TextLine(title="The password",
                        required=True)


class IUsersFolder(IContainer):
    """
    An container that holds all users, keyed by username.
    """
    contains(IUser)


class NoUserFound(ValueError):
    """
    An error raise when the user doesn't exist.
    """
