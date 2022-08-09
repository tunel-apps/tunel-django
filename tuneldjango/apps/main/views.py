from django.shortcuts import render, redirect
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from tuneldjango.apps.users.decorators import user_agree_terms

from tuneldjango.apps.main.models import Project
from tuneldjango.apps.main.forms import (
    ProjectForm,
    FormTemplateForm,
)

## Projects


@login_required
@user_agree_terms
def project_details(request, uuid):
    """Return a project, or 404."""
    try:
        project = Project.objects.get(uuid=uuid)
        return render(
            request, "projects/project_details.html", context={"project": project}
        )
    except Project.DoesNotExist:
        raise Http404


@login_required
@user_agree_terms
def user_projects(request):
    """Return a user listing of projects"""
    projects = None
    if request.user.group is not None:
        projects = Project.objects.filter(group=request.user.group)
    return all_projects(request, projects)


@login_required
@user_agree_terms
def all_projects(request, projects=None):
    """Return a project, or 404."""
    if projects is None:
        projects = Project.objects.all()
    return render(request, "projects/all_projects.html", context={"projects": projects})


@login_required
@user_agree_terms
def new_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.group = request.user.group
            project.save()
            return redirect("project_details", uuid=project.uuid)
    else:
        form = ProjectForm()
    return render(request, "projects/new_project.html", {"form": form})


## Form Templates


@login_required
@user_agree_terms
def edit_form_template(request, uuid):
    """edit a form template"""
    try:
        project = Project.objects.get(uuid=uuid)
    except Project.DoesNotExist:
        raise Http404

    if request.method == "POST":

        # If the form already belongs to another group
        if project.group != None and project.group != request.user.group:
            messages.warning(
                request,
                "You are not allowed to edit a form not owned by your group.",
            )
            return redirect("index")

        # Get standard form fields
        form = FormTemplateForm(request.POST)

        if form.is_valid():
            template = form.save(commit=False)
            template.save()
            project.form = form
            project.save()

            return redirect("group_details", uuid=project.group.id)

        # Not valid - return to page to populate
        else:
            return render(
                request,
                "projects/edit_form_template.html",
                {"form": form, "project": project},
            )
    else:
        form = FormTemplateForm()
        if project.form is not None:
            form = FormTemplateForm(initial=model_to_dict(project.form))
    return render(
        request,
        "projects/edit_form_template.html",
        {"form": form, "project": project},
    )


@login_required
@user_agree_terms
def view_project_form(request, uuid):
    try:
        project = Project.objects.get(uuid=uuid)
        form = FormTemplateForm(initial=model_to_dict(project.form))

        # If the form already belongs to another group
        if project.group != None and project.group != request.user.group:
            messages.warning(
                request,
                "You are not allowed to edit a form not owned by your group.",
            )
            return redirect("index")

        if project.form == None:
            messages.info(request, "This project does not have a form started yet.")
            return redirect("project_details", project.uuid)
        return render(
            request,
            "projects/view_project_form.html",
            context={
                "project": project,
                "form": form,
                "disabled": True,
                "strategies": project.form.implement_strategy.all(),
            },
        )
    except Project.DoesNotExist:
        raise Http404
