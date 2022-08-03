from django.urls import path
from tuneldjango.apps.main import views


urlpatterns = [
    # Projects
    path("projects/", views.all_projects, name="all_projects"),
    path("u/projects/", views.user_projects, name="user_projects"),
    path("projects/new/", views.new_project, name="new_project"),
    path("project/<uuid:uuid>/", views.project_details, name="project_details"),
    path(
        "project/forms/<uuid:uuid>/edit",
        views.edit_form_template,
        name="edit_form_template",
    ),
    path(
        "project/forms/<uuid:uuid>/", views.view_project_form, name="view_project_form"
    ),
]
