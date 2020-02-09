from zope import interface


class IApplicationSettings(interface.Interface):
    """
    An object stores the global settings, should be registered as utility.
    """


class IApplicationServer(interface.Interface):
    pass


class InvalidSiteError(Exception):
    pass
