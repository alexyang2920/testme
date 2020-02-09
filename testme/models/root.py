from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import ALL_PERMISSIONS

from zope import interface

from zope.site.folder import Folder

from testme.models.interfaces import IApplicationRoot

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IApplicationRoot)
class ApplicationRootFolder(Folder):

    __acl__ = (
        (Allow, Authenticated, ALL_PERMISSIONS),
    )
