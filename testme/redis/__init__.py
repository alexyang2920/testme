import redis

from zope import component
from zope import interface


class IRedisClient(interface.Interface):
    pass


@interface.implementer(IRedisClient)
class RedisClient(object):

    def __init__(self, host='localhost', port=6379, db=0):
        self._cli = redis.Redis(host=host,
                                port=port,
                                db=db)
