from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import ALL_PERMISSIONS

from zope import interface

from zope.container.folder import Folder

from testme.models.interfaces import IApplicationRoot


APP_ROOT_KEY = 'app_root'
USERS = 'users'


@interface.implementer(IApplicationRoot)
class ApplicationRoot(Folder):

    __acl__ = (
        (Allow, Authenticated, ALL_PERMISSIONS),
    )
