from pyramid.view import view_config

from testme.jira.interfaces import ITicketContainer

from testme.views.base import BaseTemplateView


@view_config(renderer='json', 
             context=ITicketContainer,
             request_method='GET')
class GetTicketsView(BaseTemplateView):

    def __call__(self):
        return [x for x in self.context.values()]
