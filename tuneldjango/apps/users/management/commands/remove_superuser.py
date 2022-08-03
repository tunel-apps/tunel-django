from tuneldjango.apps.users.models import User
from django.core.management.base import BaseCommand, CommandError

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """remove a superuser"""

    def add_arguments(self, parser):
        parser.add_argument(dest="username", nargs=1, type=str)

    help = "Remove superuser privileges."

    def handle(self, *args, **options):
        if options["username"] is None:
            raise CommandError("Please provide a username.")

        logger.debug("Username: %s" % options["username"][0])
        try:
            user = User.objects.get(username=options["username"][0])
        except User.DoesNotExist:
            raise CommandError("This username does not exist.")

        if user.is_superuser is False:
            raise CommandError("This user already is not a superuser.")
        else:
            user.is_superuser = False
            print("%s is no longer a superuser." % user.username)
            user.save()
