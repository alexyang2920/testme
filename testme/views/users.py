from pyramid.view import view_config

from testme.models.interfaces import IUsersFolder
from testme.views.base import BaseTemplateView


@view_config(renderer='json', 
             context=IUsersFolder, 
             request_method='GET')
class UsersListPage(BaseTemplateView):

    def __call__(self):
        return [x for x in self.context.values()]
