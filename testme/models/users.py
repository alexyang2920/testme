from persistent import Persistent

from zope import component
from zope import interface
from zope.container.folder import Folder
from zope.container.contained import Contained
from zope.schema.fieldproperty import createFieldProperties

from testme.models.interfaces import IUser
from testme.models.interfaces import IUsersFolder


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
class User(Persistent, Contained):

    createFieldProperties(IUser)


def register_user(username, password):
    user = User(username, password)
    users = component.getUtility(IUsersFolder)
    return users.storeUser(user)


def check_credentials(username, password):
    if username=='admin' and password == 'admin':
        return True
    return False
