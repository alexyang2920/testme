from zc.intid.utility import IntIds

from zope import component

from zope.component.hooks import setHooks
from zope.component.hooks import site as set_site

from zope.generations.generations import SchemaManager

from zope.site.site import LocalSiteManager
from zope.site.folder import rootFolder

from testme.models import ApplicationRoot

from testme.models.interfaces import IApplicationRoot

from testme.models import APP_ROOT_KEY
from testme.models import USERS
from testme.models import INTIDS

from testme.models.users import UsersFolder
from testme.models.index import install_users_catalog
from zope.intid.interfaces import IIntIds as zope_IIntIds
from zc.intid.interfaces import IIntIds as zc_IIntIds


generation = 0

logger = __import__('logging').getLogger(__name__)


class AppSchemaManager(SchemaManager):

    def __init__(self):
        super(AppSchemaManager, self).__init__(generation=generation,
                                               minimum_generation=generation,
                                               package_name='testme.generations')

def install_users(root_folder):
    if USERS not in root_folder:
        root_folder[USERS] = UsersFolder()
    return root_folder[USERS]


def install_intids(root_folder):
    if INTIDS not in root_folder:
        root_folder[INTIDS] = intids = IntIds(attribute="_intid")
        component.getSiteManager().registerUtility(intids, zope_IIntIds)
        component.getSiteManager().registerUtility(intids, zc_IIntIds)
    return root_folder[INTIDS]


def evolve(context):
    logger.info('Installing root folders via schema manager')
    conn = context.connection
    root = conn.root()

    # Use getSiteManager from the siteinfo.
    setHooks()

    # root folder
    root_folder = rootFolder()
    root['Application'] = root_folder
    conn.add(root_folder)
    assert root_folder._p_jar is conn

    # site
    site = ApplicationRoot()
    site.__name__ = APP_ROOT_KEY
    root_folder[APP_ROOT_KEY] = site
    conn.add(site)
    assert site.__parent__ is root_folder
    assert site._p_jar is conn
    assert IApplicationRoot.providedBy(site) is True

    # site manager.
    siteManager = LocalSiteManager(site)
    site.setSiteManager(siteManager)
    conn.add(siteManager)
    assert siteManager.__parent__ is site
    assert siteManager.__name__ == '++etc++site', 'bad site manager.'

    with set_site(site):
        assert component.getSiteManager() is siteManager, 'no hooks?'
        install_intids(site)
        install_users(site)
        install_users_catalog(site)

    logger.info("Finish installing root folders.")
