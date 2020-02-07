from zope.generations.generations import SchemaManager

from testme.models import ApplicationRoot
from testme.models import APP_ROOT_KEY
from testme.models import USERS
from testme.models.users import UsersFolder

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


def evolve(context):
    logger.info('Installing root folders via schema manager')
    root = context.connection.root()
    app_root = root[APP_ROOT_KEY] = ApplicationRoot()
    install_users(app_root)
    logger.info("Finish install root folders.")
