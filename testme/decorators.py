
LINKS = 'links'

class Link(object):

    def __init__(self, rel, href, method=None):
        self.rel = rel
        self.href = href
        self.method = method

    def __json__(self, unused_request):
        result = {'rel': self.rel,
                  'href': self.href}
        if self.method:
            result['method'] = self.method
        return result


class AbstractDecorator(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def decorate(self, result):
        raise NotImplemented()
