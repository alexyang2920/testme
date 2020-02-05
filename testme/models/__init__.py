from persistent.mapping import PersistentMapping
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import ALL_PERMISSIONS


class Root(PersistentMapping):
    __parent__ = __name__ = None

    __acl__ = (
        (Allow, Authenticated, ALL_PERMISSIONS),
    )

def appmaker(zodb_root):
    if 'app_root' not in zodb_root:
        app_root = Root()
        zodb_root['app_root'] = app_root
    return zodb_root['app_root']
