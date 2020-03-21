from pyramid.view import view_config
from pyramid import httpexceptions as hexc

from zope import component

from testme.jira.interfaces import IProjectContainer, IProject
from testme.jira.model import Project

from testme.models.interfaces import IUsersFolderFactory
from testme.views.base import BaseTemplateView, BaseView

from testme.views.utils import raise_json_error


@view_config(renderer='../../templates/jira/projects.pt', 
             context=IProjectContainer,
             request_method='GET',
             name="list")
class ProjectsPageView(BaseTemplateView):

    def __call__(self):
        return {}


@view_config(renderer='../../templates/jira/create_project.pt', 
             context=IProjectContainer,
             request_method='GET',
             name="create")
class ProjectCreatePageView(BaseTemplateView):

    def __call__(self):
        return {}

@view_config(renderer='../../templates/jira/project.pt',
             context=IProject,
             request_method='GET',
             name="detail")
class ProjectDetailPageView(BaseTemplateView):

    def __call__(self):
        return {}


@view_config(renderer='json', 
             context=IProjectContainer,
             request_method='GET')
class GetProjectsView(BaseTemplateView):

    def __call__(self):
        return [x for x in self.context.values()]


@view_config(renderer='json', 
             context=IProjectContainer, 
             request_method='POST')
class CreateProjectView(BaseView):

    def __call__(self):
        project_name = self.get_value('project_name')
        project_type = self.get_value('project_type')
        project_lead = self.get_value('project_lead')
        
        users = component.getUtility(IUsersFolderFactory)()
        project_lead = users.getUser(project_lead)
        if not project_lead:
            raise_json_error(hexc.HTTPUnprocessableEntity,
                             "Lead does not exist.")

        proj = Project(project_name=project_name,
                       project_type=project_type,
                       project_lead=project_lead)
        self.context.store_project(proj)
        return {}

