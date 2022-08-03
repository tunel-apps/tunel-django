from django.contrib import admin
from django.urls import include, path
from tuneldjango.apps.main import urls as main_urls
from tuneldjango.apps.base import urls as base_urls
from tuneldjango.apps.users import urls as user_urls

# Customize admin title, headers
admin.site.site_header = "tunel-django Administration"
admin.site.site_title = "tunel-django Admin"
admin.site.index_title = "tunel-django administration"

# Configure custom error pages
handler404 = "tuneldjango.apps.base.views.handler404"
handler500 = "tuneldjango.apps.base.views.handler500"

urlpatterns = [
    path("", include(base_urls)),
    path("", include(main_urls)),
    path("", include(user_urls)),
    path("admin/", admin.site.urls),
]
