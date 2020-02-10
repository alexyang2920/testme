from pyramid.interfaces import IRequest

from pyramid_zodbconn import get_connection

from zope import interface
from zope import component

from zope.interface.interfaces import IComponentLookup

from testme.models import APP_ROOT_KEY
from testme.models import USERS

from testme.models.interfaces import IApplicationRoot
from testme.models.interfaces import IUsersFolderFactory

from testme.interfaces import IApplicationServer
from pyramid.traversal import find_interface

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IComponentLookup)
def _site_manager_from_context(context):
    # component.getAllUtilitiesRegisteredFor needs this,
    # may have other better solution.
    app_root = find_interface(context, IApplicationRoot)
    return app_root.getSiteManager()


@component.adapter(IRequest)
@interface.implementer(IApplicationRoot)
def _application_root(request):
    conn = get_connection(request)
    return conn.root()[APP_ROOT_KEY]


@interface.implementer(IUsersFolderFactory)
def get_users_folder(appRoot=None):
    if appRoot is None:
        appRoot = component.getUtility(IApplicationServer).app_root
    return appRoot[USERS]
