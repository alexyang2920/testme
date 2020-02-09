from zope import component
from zope import interface
from zope.processlifetime import DatabaseOpened
from zope.processlifetime import DatabaseOpenedWithRoot

from ZODB.interfaces import IDatabase
from ZODB.interfaces import IConnection

from zope.event import notify

from testme.interfaces import IApplicationServer
from testme.interfaces import InvalidSiteError

from testme.models import APP_ROOT_KEY


@interface.implementer(IApplicationServer)
class ApplicationServer(object):

    def __init__(self, dbs):
        self.open_dbs(dbs)

    @property
    def app_root(self):
        lsm = component.getSiteManager()
        conn = IConnection(lsm, None)
        if conn:
            return conn.root()[APP_ROOT_KEY]

        raise InvalidSiteError("Using app server outside of site manager")

    def open_dbs(self, dbs):
        # register dbs as utility
        for name, db in dbs.items():
            if not IDatabase.providedBy(db):
                interface.directlyProvides(db, IDatabase)
            component.provideUtility(db, IDatabase, name)

        # Trigger zope.generations
        root_db = component.getUtility(IDatabase)
        notify(DatabaseOpened(root_db))
        notify(DatabaseOpenedWithRoot(root_db))
