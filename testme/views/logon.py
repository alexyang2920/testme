from pyramid import httpexceptions as hexc
from pyramid.view import view_config

from pyramid.security import remember
from pyramid.security import forget

from urllib.parse import urljoin

from testme.models import ApplicationRoot
from testme.models.users import check_credentials
from testme.models.users import register_user

from testme.views.base import BaseView
from testme.views.base import BaseTemplateView
from testme.views.utils import raise_json_error


@view_config(renderer='../templates/login.pt', 
             context=ApplicationRoot, 
             request_method='GET',
             name='login')
class LoginPage(BaseTemplateView):

    def __call__(self):
        if self.request.authenticated_userid:
            return hexc.HTTPFound(location='/')
        success = self.request.params.get('success') or '/'
        return {'success': success}


@view_config(renderer='json', 
             context=ApplicationRoot, 
             request_method='POST',
             name='login')
class LoginView(BaseView):

    def __call__(self):
        username = self.get_value('username')
        password = self.get_value('password')
        if not check_credentials(username, password):
            raise_json_error(hexc.HTTPUnprocessableEntity,
                             "Invalid credentials.")
        
        headers = remember(self.request, username)
        self.request.response.headerlist.extend(headers)

        success = self.request.params.get('success') or '/'
        return {'redirect': success}


@view_config(context=ApplicationRoot, 
             request_method='GET',
             name='logout')
class LogoutView(BaseView):

    def __call__(self):
        self.request.session.invalidate()
        headers = forget(self.request)
        url = urljoin(self.request.application_url, 'login')
        return hexc.HTTPFound(location=url,
                              headers=headers)


@view_config(renderer='../templates/register.pt', 
             context=ApplicationRoot, 
             request_method='GET',
             name='register')
class RegisterPage(BaseTemplateView):
    
    def __call__(self):
        return {}


@view_config(renderer='json', 
             context=ApplicationRoot, 
             request_method='POST',
             name='register')
class RegisterView(BaseView):

    def __call__(self):
        username = self.get_value('username')
        password = self.get_value('password')
        try:
            register_user(username, password)
        except KeyError:
            raise_json_error(hexc.HTTPUnprocessableEntity,
                             'Username is not available.')
        url = urljoin(self.request.application_url, 'login')
        return {'redirect': url}
