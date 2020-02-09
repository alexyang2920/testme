from pyramid_zodbconn import get_connection

from zope.component.hooks import setSite

from testme import models


def setup(env):
    request = env['request']

    # start a transaction
    request.tm.begin()
    conn = get_connection(request)

    env['tm'] = request.tm
    env['models'] = models
    env['conn'] = conn.root()
    env['testme'] = site = conn.root()[models.APP_ROOT_KEY]

    setSite(site)
