from zope import interface

from zope.annotation.interfaces import IAttributeAnnotatable

from zope.catalog.interfaces import ICatalog

from zope.container.interfaces import IContainer
from zope.container.constraints import contains
from zope.location.interfaces import IContained

from zope.schema import TextLine
from zope.schema import Float


class IApplicationRoot(IContainer):
    """
    Marker interface that indicates an IRootFolder,
    also should represent the pyramid root factory.
    """


class IUser(IContained, IAttributeAnnotatable):

    username = TextLine(title="The username",
                        required=True)

    password = TextLine(title="The password",
                        required=True)

    email = TextLine(title="The email",
                     required=True)

    last_verified = Float(title="The UTC time stamp when this user is email verified.",
                          required=False)


class IUsersFolder(IContainer):
    """
    An container that holds all users, keyed by username.
    """
    contains(IUser)


class IUsersFolderFactory(interface.Interface):
    """
    An object that is called to return an IUsersFolder.
    """


class NoUserFound(ValueError):
    """
    An error raise when the user doesn't exist.
    """

class IUsersCatalog(ICatalog):
    """
    Catalog that indexing users objects.
    """
