from zope.component.hooks import site as set_site

from testme.models import APP_ROOT_KEY
from testme.blog.model import BlogContainer

logger = __import__('logging').getLogger(__name__)

generation = 3

BLOGS = 'blogs'


def install_blogs(root_folder):
    if BLOGS not in root_folder:
        root_folder[BLOGS] = BlogContainer()
    return root_folder[BLOGS]


def evolve(context):
    logger.info('Installing blogs.')
    conn = context.connection
    root = conn.root()

    site =root['Application'][APP_ROOT_KEY]
    with set_site(site):
        install_blogs(site)
