from django.urls import path, include
from filebrowser.sites import site

# Browse entire media root /var/www/data
site.directory = ""

urlpatterns = [
    path("", site.urls),
    path("grappelli/", include("grappelli.urls")),
]
