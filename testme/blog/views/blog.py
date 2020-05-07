from pyramid.view import view_config
from pyramid import httpexceptions as hexc

from zope import component

from testme.blog.interfaces import IBlogContainer, IBlog
from testme.blog.model import Blog

from testme.models.interfaces import IUsersFolderFactory
from testme.views.base import BaseTemplateView, BaseView

from testme.views.utils import raise_json_error


@view_config(renderer='../../templates/blog/blogs.pt', 
             context=IBlogContainer,
             request_method='GET',
             name="list")
class BlogsPageView(BaseTemplateView):

    def __call__(self):
        return {}
