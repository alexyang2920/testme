"""
Test views
"""
from pyramid.view import view_config
from testme.models.interfaces import IApplicationRoot

from .base import BaseView
from ..mailer import queue_html_text_email

@view_config(renderer='json', 
             context=IApplicationRoot, 
             request_method='GET',
             name='test')
class TestEmail(BaseView):

    def __call__(self):
        queue_html_text_email(template="testme:email_templates/welcome",
                              subject="Welcome to TestMe",
                              recipients=['1032442805g@gmail.com'],
                              template_args={'name': "Yang"})
        return {}
