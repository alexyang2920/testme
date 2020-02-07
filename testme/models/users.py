from persistent import Persistent

from zope import interface
from zope.container.folder import Folder
from zope.container.contained import Contained
from zope.schema.fieldproperty import createFieldProperties

from testme.models.base import Base

from testme.models.interfaces import IUser
from testme.models.interfaces import IUsersFolder

from testme.models.utils import get_users_folder


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

    def __init__(self, username, password):
        self.username = username
        self.password = password


def _hash_password(password):
    # TODO encoding it
    # may ref https://www.vitoshacademy.com/hashing-passwords-in-python/
    return password


def register_user(username, password):
    user = User(username, _hash_password(password))
    folder = get_users_folder()
    return folder.storeUser(user)


def check_credentials(username, password):
    folder = get_users_folder()
    if username not in folder:
        return False

    user = folder.getUser(username)
    return bool(_hash_password(password) == user.password)
