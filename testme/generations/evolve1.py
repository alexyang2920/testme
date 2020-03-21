from zope.component.hooks import site as set_site

from testme.models import APP_ROOT_KEY
from testme.jira.model import JiraContainer
from testme.jira.model import ProjectContainer
from testme.jira.model import TicketContainer

logger = __import__('logging').getLogger(__name__)

generation = 1


JIRA = 'jira'
PROJECTS = 'projects'
TICKETS = 'tickets'


def install_jira(root_folder):
    if JIRA not in root_folder:
        root_folder[JIRA] = jira = JiraContainer()
        jira[PROJECTS] = ProjectContainer()
        jira[TICKETS] = TicketContainer()
    return root_folder[JIRA]


def evolve(context):
    logger.info('Installing jira.')
    conn = context.connection
    root = conn.root()

    site =root['Application'][APP_ROOT_KEY]
    with set_site(site):
        install_jira(site)
