from zope.component.hooks import site as set_site

from testme.models import APP_ROOT_KEY
from testme.dictionary.model import WordContainer

logger = __import__('logging').getLogger(__name__)

generation = 2

WORDS = 'words'


def install_words(root_folder):
    if WORDS not in root_folder:
        root_folder[WORDS] = WordContainer()
    return root_folder[WORDS]


def evolve(context):
    logger.info('Installing words.')
    conn = context.connection
    root = conn.root()

    site =root['Application'][APP_ROOT_KEY]
    with set_site(site):
        install_words(site)
