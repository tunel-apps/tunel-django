from django.core.management.base import BaseCommand, CommandError

from tuneldjango.apps.users.models import User

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    add a superuser
    """

    def add_arguments(self, parser):
        parser.add_argument(dest="username", nargs="*")

    help = "Generates a superuser"

    def handle(self, *args, **options):
        # TODO can add their email here for notifications, also as tunel arg
        if not options["username"] or len(options["username"]) != 2:
            raise CommandError("Please provide a username and password")

        logger.debug("Username: %s" % options["username"][0])

        try:
            user = User.objects.create_superuser(
                options["username"][0],
                "user@noreply.tunel-app.com",
                options["username"][1],
            )
            user.is_staff = True
            user.save()
        except Exception as e:
            print("cannot create superuser: %s" % e)
