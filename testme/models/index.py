import BTrees

from zope import interface
from zope import component

from zope.catalog.catalog import Catalog
from zope.catalog.attribute import AttributeIndex as RawAttributeIndex

from zope.index.field import FieldIndex

from testme.models.interfaces import IUser
from testme.models.interfaces import IUsersCatalog

USERS_CATALOG_NAME = '++catalog++users'
IX_USERNAME = 'username'
IX_EMAIL = 'email'


class AttributeIndex(RawAttributeIndex, FieldIndex):

    family = BTrees.family32


class UsernameIndex(AttributeIndex):

    default_interface = IUser
    default_field_name = 'username'


class EmailIndex(AttributeIndex):

    default_interface = IUser
    default_field_name = 'email'


class BaseCatalog(Catalog):

    family = BTrees.family32

    def index(self, ob):
        raise NotImplementedError()


@interface.implementer(IUsersCatalog)
class UsersCatalog(BaseCatalog):
    pass


def install_users_catalog(app_root):
    if USERS_CATALOG_NAME not in app_root:
        catalog = app_root[USERS_CATALOG_NAME] = UsersCatalog()
        for index_name, index_value in ((IX_USERNAME, UsernameIndex),
                                        (IX_EMAIL, EmailIndex)):
            catalog[index_name] = index_value()

        component.provideUtility(catalog, IUsersCatalog)

    return app_root[USERS_CATALOG_NAME]
