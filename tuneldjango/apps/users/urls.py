from django.urls import path
from django.urls import include

import tuneldjango.apps.users.views as views

urlpatterns = [
    # Twitter, and social auth
    path("login/", views.login, name="login"),
    path("accounts/login/", views.login),
    path("logout/", views.logout, name="logout"),
    path("password/", views.change_password, name="change_password"),
    path("terms/agree/", views.agree_terms, name="agree_terms"),
    path("delete/", views.delete_account, name="delete_account"),  # delete account
    path("u/profile/", views.view_profile, name="profile"),
    # Groups
    path("group/<int:uuid>/", views.group_details, name="group_details"),
    path("groups/", views.all_groups, name="all_groups"),
    path("u/group/", views.user_group, name="user_group"),
    # Users
    path("u/invite/", views.invite_users, name="invite_users"),
    path("u/invite/<uuid:uuid>/", views.invited_user, name="invited_user"),
    # We don't currently have a reason for one user to see another user's account
    # url(r'^(?P<username>[A-Za-z0-9@/./+/-/_]+)/$',views.view_profile,name="profile"),
]
