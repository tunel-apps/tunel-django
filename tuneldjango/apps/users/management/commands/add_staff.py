from django.core.management.base import BaseCommand, CommandError

from tuneldjango.apps.users.models import User

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """add staff will add admin and manager privileges to a user.
    The super user is an admin that can access the administrative
    interface, and pretty much do anything.
    """

    def add_arguments(self, parser):
        parser.add_argument(dest="username", nargs=1, type=str)

    help = "Generates an admin"

    def handle(self, *args, **options):
        if options["username"] is None:
            raise CommandError("Please provide a username with --username")

        logger.debug("Username: %s" % options["username"])
        try:
            user = User.objects.get(username=options["username"][0])
        except User.DoesNotExist:
            raise CommandError("This username does not exist.")

        if user.is_staff is True:
            raise CommandError("This user is already staff")
        else:
            user = User.objects.add_staff(user)
            print("%s is now staff." % user.username)
