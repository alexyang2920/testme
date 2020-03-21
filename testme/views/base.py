from pyramid import httpexceptions as hexc

from zope.cachedescriptors.property import Lazy

from testme.views.utils import raise_json_error


class BaseView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy
    def params(self):
        return self.request.params

    @Lazy
    def body_params(self):
        return self.readInput()

    def readInput(self):
        try:
            return self.request.json_body
        except ValueError:
            raise_json_error(hexc.HTTPUnprocessableEntity,
                             "Invalid json body.")

    def get_param(self, name, params=None, required=True):
        params = self.params if params is None else params
        value = params.get(name)
        value = value.strip() if value else value
        if not value and required:
            raise_json_error(hexc.HTTPUnprocessableEntity,
                             'Missing %s.' % name)
        return value

    def get_value(self, name, params=None, required=True):
        params = self.body_params if params is None else params
        value = params.get(name)
        if isinstance(value, str):
            value = value.strip() or None

        if value is None and required:
            raise_json_error(hexc.HTTPUnprocessableEntity,
                             'Missing %s.' % name)
        return value


class BaseTemplateView(BaseView):

    logged_in = None
    def __init__(self, context, request):
        BaseView.__init__(self, context, request)

        self.logged_in = bool(self.request.authenticated_userid)
