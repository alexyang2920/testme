from pyramid.view import view_config

from testme.views.base import BaseTemplateView

from testme.models.interfaces import IApplicationRoot


@view_config(renderer="../templates/chat.pt",
             context=IApplicationRoot, 
             request_method='GET',
             permission='view',
             name="chat")
class ChatView(BaseTemplateView):

    def __call__(self):
        return {}
