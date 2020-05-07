from zope.container.interfaces import IContainer
from zope.location.interfaces import IContained


class IBlogContainer(IContainer):
    pass


class IBlog(IContained):
    pass