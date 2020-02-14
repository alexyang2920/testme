from pyramid_zodbconn import get_connection

from zope.component.hooks import setSite
from zope.component.hooks import setHooks
from zope.component.hooks import clearSite

logger = __import__('logging').getLogger(__name__)


class site_tween(object):

    __slots__ = ('handler',)

    def __init__(self, handler):
        self.handler = handler

    def __call__(self, request):
        site = get_connection(request).root()['Application']['testme']
        setSite(site)
        try:
            return self.handler(request)
        finally:
            clearSite()

def site_tween_factory(handler, registry):
    setHooks()
    return site_tween(handler)
