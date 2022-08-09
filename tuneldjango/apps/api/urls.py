from django.urls import path
from tuneldjango.apps.api import views


urlpatterns = [
    path("joke/", views.get_joke, name="get_joke"),
    path("joke/<int:uuid>/", views.get_joke, name="get_joke"),
]
