from persistent import Persistent

from pyramid.threadlocal import get_current_request

from zope import interface
from zope.container.folder import Folder
from zope.container.contained import Contained
from zope.schema.fieldproperty import createFieldProperties

from testme.models import USERS

from testme.models.base import Base

from testme.models.interfaces import IUser
from testme.models.interfaces import IUsersFolder
from testme.models.interfaces import IApplicationRoot


@interface.implementer(IUsersFolder)
class UsersFolder(Folder):

    def storeUser(self, user):
        self[user.username] = user
        return user

    def removeUser(self, user):
        username = getattr(user, 'username', user)
        del self[username]

    def getUser(self, username):
        return self.get(username)


@interface.implementer(IUser)
class User(Base, Persistent, Contained):

    createFieldProperties(IUser)

    __json_exclude__ = ('password',)

    def __init__(self, username, password, email):
        self.username = username
        self.password = _hash_password(password)
        self.email = email


def get_users_folder(app_root=None, request=None):
    if app_root is None:
        request = request or get_current_request()
        app_root = IApplicationRoot(request)
    return app_root[USERS]


def _hash_password(password):
    # TODO encoding it
    # may ref https://www.vitoshacademy.com/hashing-passwords-in-python/
    return password


def check_credentials(username, password):
    folder = get_users_folder()
    if username not in folder:
        return False

    user = folder.getUser(username)
    return bool(_hash_password(password) == user.password)
