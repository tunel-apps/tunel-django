from django.core.exceptions import PermissionDenied


def user_is_staff_superuser(function):
    """return permission denied if a user is not staff or superuser"""

    def wrap(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
