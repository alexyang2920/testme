import time

from zope import component

from testme.interfaces import IExternalDecorator


class Base(object):
    """
    https://docs.pylonsproject.org/projects/pyramid/en/1.5-branch/narr/renderers.html#using-a-custom-json-method
    """
    def __init__(self):
        self.createdTime = time.time()
        self.lastModified = self.createdTime

    def __json__(self, request):
        json_exclude = getattr(self, '__json_exclude__', set())
        result = {k:v for k, v in self.__dict__.items()
                    if not k.startswith('_') and k not in json_exclude }

        # Inject externalization decoration,
        # may change to subscribers if necessary.
        decorator = component.queryMultiAdapter((self, request), IExternalDecorator)
        if decorator is not None:
            decorator.decorate(result)

        return result
