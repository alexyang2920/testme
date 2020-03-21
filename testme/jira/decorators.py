from urllib.parse import urljoin

from pyramid.interfaces import IRequest

from zope import interface, component

from testme.decorators import AbstractDecorator
from testme.decorators import LINKS
from testme.decorators import Link

from testme.interfaces import IExternalDecorator
from testme.jira.interfaces import IProject


@component.adapter(IProject, IRequest)
@interface.implementer(IExternalDecorator)
class ProjectDecorator(AbstractDecorator):

    def decorate(self, external):
        links = external.setdefault(LINKS, [])
        links.append(Link(rel="detail",
                          href=urljoin(self.request.resource_url(self.context), '@@detail'),
                          method="GET"))
