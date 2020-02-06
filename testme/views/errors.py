from pyramid import httpexceptions as hexc

from pyramid.view import forbidden_view_config
from pyramid.view import notfound_view_config

from testme.views.base import BaseTemplateView


def is_browser_request(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return False

    useragent = request.environ.get('HTTP_USER_AGENT', '').lower()
    if 'httpie' in useragent:
        return False

    return True


@notfound_view_config(renderer='../templates/error.pt')
class NotFoundView(BaseTemplateView):

    def __call__(self):
        self.request.response.status = 404
        return {'message': '404 Not Found.'}


@forbidden_view_config(renderer='../templates/error.pt')
class ForbiddenView(BaseTemplateView):

    def __call__(self):
        if self.request.authenticated_userid:
            return {'message': '403 Forbidden.'}

        if is_browser_request(self.request):
            success = self.request.path_qs
            return hexc.HTTPFound(location='/login?success={}'.format(success))

        self.context.status_code = 401
        return {'message': '401 Unauthorized.'}
