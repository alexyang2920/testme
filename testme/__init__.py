from pyramid.config import Configurator
from pyramid_zodbconn import get_connection

from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.session import SignedCookieSessionFactory

from zope import component

from .models import appmaker

from testme.pyramid_authentication import create_authentication_policy


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    registry = component.getGlobalSiteManager()
    with Configurator(registry=registry) as config:
        config.setup_registry(settings=settings)

        settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'
        config.include('pyramid_tm')
        config.include('pyramid_retry')
        config.include('pyramid_zodbconn')
        config.set_root_factory(root_factory)
        config.include('pyramid_chameleon')
        config.include('.routes')

        session_factory = SignedCookieSessionFactory('foo')
        config.set_session_factory(session_factory)

        # authentication policy
        config.set_authentication_policy(create_authentication_policy())

        # authorization policy
        config.set_authorization_policy(ACLAuthorizationPolicy())

        config.scan()
    return config.make_wsgi_app()
