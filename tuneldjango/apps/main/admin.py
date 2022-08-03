from django.contrib import admin
from tuneldjango.apps.main.models import Project, FormTemplate


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "group",
        "description",
        "form",
        "contact",
    )


class FormTemplateAdmin(admin.ModelAdmin):
    list_display = (
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
        "results_other",
    )


admin.site.register(FormTemplate, FormTemplateAdmin)
admin.site.register(Project, ProjectAdmin)
