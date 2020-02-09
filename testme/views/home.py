from pyramid.view import view_config

from testme.models.interfaces import IApplicationRoot
from testme.views.base import BaseTemplateView


@view_config(renderer='../templates/home.pt', 
             context=IApplicationRoot, 
             request_method='GET',
             permission='view')
class HomePage(BaseTemplateView):

    def __call__(self):
        return {}
