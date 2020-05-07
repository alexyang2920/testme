from zope import interface

from zope.container.folder import Folder
from zope.container.contained import Contained

from zope.schema.fieldproperty import createFieldProperties

from persistent import Persistent

from testme.models.base import Base
from testme.blog.interfaces import IBlogContainer,IBlog


@interface.implementer(IBlogContainer)
class BlogContainer(Folder):
    pass


@interface.implementer(IBlog)
class Blog(Base, Persistent, Contained):

    createFieldProperties(IBlog)
