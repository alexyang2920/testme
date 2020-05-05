from pyramid import httpexceptions as hexc
from pyramid.view import view_config

from pyramid.security import remember
from pyramid.security import forget

from urllib.parse import urljoin

from zope.cachedescriptors.property import Lazy

from testme.models.interfaces import IApplicationRoot

from testme.models.users import User
from testme.models.users import check_credentials
from testme.models.users import get_users_folder

from testme.models.index import query_users

from testme.views.base import BaseView
from testme.views.base import BaseTemplateView
from testme.views.utils import raise_json_error


@view_config(renderer='../templates/login.pt', 
             context=IApplicationRoot, 
             request_method='GET',
             name='login')
class LoginPage(BaseTemplateView):

    def __call__(self):
        if self.request.authenticated_userid:
            return hexc.HTTPFound(location='/')
        success = self.request.params.get('success') or '/testme'
        return {'success': success}


@view_config(renderer='json', 
             context=IApplicationRoot, 
             request_method='POST',
             name='login')
class LoginView(BaseView):

    def doLogin(self):
        username = self.get_value('username')
        password = self.get_value('password')
        if not check_credentials(username, password):
            raise_json_error(hexc.HTTPUnprocessableEntity,
                             "Invalid credentials.")

        headers = remember(self.request, username)
        self.request.response.headerlist.extend(headers)
        user = get_users_folder().get(username)
        return user

    def __call__(self):
        self.doLogin()
        success = self.request.params.get('success') or '/testme'
        return {'redirect': success}


@view_config(renderer='json', 
             context=IApplicationRoot, 
             request_method='POST',
             name='jsonLogin')
class LoginWithUserResultView(LoginView):

    def __call__(self):
        return self.doLogin()


@view_config(context=IApplicationRoot, 
             request_method='GET',
             name='logout')
class LogoutView(BaseView):

    def __call__(self):
        self.request.session.invalidate()
        headers = forget(self.request)
        url = urljoin(self.request.application_url, '/testme/login')
        return hexc.HTTPFound(location=url,
                              headers=headers)


@view_config(renderer='json',
             context=IApplicationRoot, 
             request_method='GET',
             name='jsonLogout')
class LogoutWithJsonView(BaseView):

    def __call__(self):
        self.request.session.invalidate()
        headers = forget(self.request)
        self.request.response.headerlist.extend(headers);
        return {}


@view_config(renderer='../templates/register.pt', 
             context=IApplicationRoot, 
             request_method='GET',
             name='register')
class RegisterPage(BaseTemplateView):
    
    def __call__(self):
        return {}


@view_config(renderer='json', 
             context=IApplicationRoot, 
             request_method='POST',
             name='register')
class RegisterView(BaseView):

    @Lazy
    def users_folder(self):
        return get_users_folder(app_root=self.context)

    def __call__(self):
        username = self.get_value('username')
        password = self.get_value('password')
        email = self.get_value('email')
        if username in self.users_folder:
            raise_json_error(hexc.HTTPUnprocessableEntity,
                             'Username is not available: %s.' % username)

        if query_users(email):
            raise_json_error(hexc.HTTPUnprocessableEntity,
                             'Email has been signed up by other user: %s.' % email)

        user = User(username=username,
                    password=password,
                    email=email)

        self.users_folder.storeUser(user)

        url = urljoin(self.request.application_url, '/testme/login')
        return {'redirect': url}
