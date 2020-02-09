from pyramid.config import Configurator
from pyramid_zodbconn import get_connection

from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.session import SignedCookieSessionFactory

from pyramid.tweens import EXCVIEW

from zope import component

from zope.component.hooks import setHooks

from testme.models.interfaces import IApplicationRoot

from testme.pyramid_authentication import create_authentication_policy

from testme.appserver import ApplicationServer

from testme.interfaces import IApplicationSettings
from testme.interfaces import IApplicationServer


def root_factory(request):
    return IApplicationRoot(request)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # z3c registry required this.
    # setHooks()

    registry = component.getGlobalSiteManager()
    with Configurator(registry=registry) as config:
        config.setup_registry(settings=settings)

        component.getGlobalSiteManager().registerUtility(settings, IApplicationSettings)

        settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'
        config.include('pyramid_tm')
        config.include('pyramid_retry')
        config.include('pyramid_zodbconn')

        config.add_tween('testme.tweens.site_tween_factory',
                         over=EXCVIEW)

        config.set_root_factory(root_factory)
        config.include('pyramid_chameleon')
        config.include('pyramid_mako')
        config.include('.routes')

        config.include('pyramid_zcml')
        config.load_zcml('configure.zcml')

        # session factory
        session_factory = SignedCookieSessionFactory('foo')
        config.set_session_factory(session_factory)

        # authentication policy
        config.set_authentication_policy(create_authentication_policy())

        # authorization policy
        config.set_authorization_policy(ACLAuthorizationPolicy())

        config.scan()

    # register server utility, open root database connection.
    server = ApplicationServer(config.registry._zodb_databases)
    component.getGlobalSiteManager().registerUtility(server, IApplicationServer)

    return config.make_wsgi_app()
