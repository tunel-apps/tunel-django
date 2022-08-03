from tuneldjango.apps.main.models import Project, FormTemplate
from django import forms


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        # Group is associated to the user creating the project
        fields = ("name", "description", "contact")

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class FormTemplateForm(forms.ModelForm):
    """A form to populate a project template. Commented out fields are
    not required for stage 1
    """

    stage = 1

    class Meta:
        model = FormTemplate
        fields = (
            "name",
            "start_date",
            "end_date",
            "target_audience_disciplines",
            "target_audience_roles",
            "target_audience_across_orgs",
            "target_audience_within_org",
            "target_audience_teams_across_orgs",
            "implement_strategy_description",
            "consider_system_factors",
            "consider_org_factors",
            "consider_clinical_factors",
            "consider_sustainment_strategy",
            "outcome_reach",
            "outcome_effectiveness",
            "outcome_adoption",
            "outcome_quality",
            "outcome_cost",
            "outcome_maintenance",
            "outcome_other",
            "implementation_recruited",
            "implementation_participants",
            "implementation_enrolled",
            "implementation_completing_half",
            "implementation_completing_majority",
            "results_reach",
            "results_effectiveness",
            "results_adoption",
            "results_quality",
            "results_cost",
            "results_maintenance",
            "results_other",
        )

    def __init__(self, *args, **kwargs):
        super(FormTemplateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
