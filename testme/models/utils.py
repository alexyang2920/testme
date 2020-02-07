from pyramid.threadlocal import get_current_request

from testme.models import USERS
from testme.models.interfaces import IApplicationRoot


def get_users_folder(request=None):
    request = request or get_current_request()
    approot = IApplicationRoot(request)
    return approot[USERS]
