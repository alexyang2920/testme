from pyramid.interfaces import IRequest

from pyramid_zodbconn import get_connection

from zope import interface
from zope import component

from testme.models import APP_ROOT_KEY

from testme.models.interfaces import IApplicationRoot

logger = __import__('logging').getLogger(__name__)


@component.adapter(IRequest)
@interface.implementer(IApplicationRoot)
def _application_root(request):
    conn = get_connection(request)
    return conn.root()[APP_ROOT_KEY]
