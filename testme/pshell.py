from pyramid_zodbconn import get_connection

from testme import models


def setup(env):
    request = env['request']

    # start a transaction
    request.tm.begin()

    # inject some vars into the shell builtins
    env['tm'] = request.tm
    env['models'] = models
    env['app_root'] = get_connection(request).root()
