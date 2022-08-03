from django.core.management.base import BaseCommand, CommandError

from tuneldjango.apps.users.models import User
from tuneldjango.settings import NODE_NAME

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """remove staff from the server"""

    def add_arguments(self, parser):
        parser.add_argument(dest="username", nargs=1, type=str)

    help = "Removes staff priviledges for %s." % NODE_NAME

    def handle(self, *args, **options):
        if options["username"] is None:
            raise CommandError("Please provide a username with --username")

        logger.debug("Username: %s" % options["username"])

        try:
            user = User.objects.get(username=options["username"][0])
        except User.DoesNotExist:
            raise CommandError("This username does not exist.")

        if user.is_staff is False:
            raise CommandError("This user is already not staff.")
        else:
            user.is_staff = False
            user.save()
            print("%s is not longer staff." % user.username)
