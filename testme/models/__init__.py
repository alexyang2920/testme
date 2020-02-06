from persistent.mapping import PersistentMapping
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import ALL_PERMISSIONS

from .users import UsersFolder

USERS = 'users'


class ApplicationRoot(PersistentMapping):
    __parent__ = __name__ = None

    __acl__ = (
        (Allow, Authenticated, ALL_PERMISSIONS),
    )


def install_users(root):
    if USERS not in root:
        users = UsersFolder()
        users.__name__ = USERS
        root[USERS] = users
    return root[USERS]


def appmaker(zodb_root):
    if 'app_root' not in zodb_root:
        app_root = ApplicationRoot()
        zodb_root['app_root'] = app_root

        install_users(app_root)

    return zodb_root['app_root']
