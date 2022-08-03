from django.views.generic.base import TemplateView
from django.urls import path

import tuneldjango.apps.base.views as views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("terms/", views.terms_view, name="terms"),
    path("privacy-policy/", views.terms_view, name="privacy-policy"),
    path("search/", views.search_view, name="search"),
    path("searching/", views.run_search, name="running_search"),
    path("search/<str:query>/", views.search_view, name="search_query"),
    path("robots.txt",
        TemplateView.as_view(
            template_name="base/robots.txt", content_type="text/plain"
        ),
    ),
]
