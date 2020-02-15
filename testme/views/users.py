from pyramid.view import view_config
from pyramid import httpexceptions as hexc

from testme.models.interfaces import IUser
from testme.models.interfaces import IUsersFolder
from testme.views.base import BaseTemplateView, BaseView


@view_config(renderer='json', 
             context=IUsersFolder,
             request_method='GET')
class UsersGetView(BaseTemplateView):

    def __call__(self):
        return [x for x in self.context.values()]


@view_config(renderer='json', 
             context=IUser,
             request_method='GET')
class UserGetView(BaseView):

    def __call__(self):
        return self.context


@view_config(renderer='json', 
             context=IUser,
             request_method='DELETE')
class UserDeletionView(BaseView):

    def __call__(self):
        folder = self.context.__parent__
        folder.removeUser(self.context)
        return hexc.HTTPNoContent()
