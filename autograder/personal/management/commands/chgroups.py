"""
Creates permissions and groups automatically with custom command `chgroups`.
Loads fixtures stored in personal/fixtures for auth tables into
/personal/fixtures/.

Used in manage.py to automate initial set-up with `add`. `update` allows
for automated storage in pre-defined filename/location to avoid inconsistency
from typo and provide minor ease of use in command length.

Superuser account is stored in 'init_superuser.json'. Superuser is updated
by pulling user details, `update` will refresh credentials if needed.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core import serializers
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates or updates default permission groups for groups.'

    # Allow user to specify `chgroups add`, as in first populating the database
    # with the user and admin models, or `chgroups update`, which updates the
    # fixtures which are loaded when the add command is executed.
    def add_arguments(self, parser):
        parser.add_argument(
          'action',
          type=str,
          help='Specify "load" to load permissions, "update" to store \
            any newly created groups or permissions.')

    def handle(self, *args, **kwargs):
        arg = kwargs['action']
        if arg != 'update' and arg != 'load':
            print("ERROR: Invalid argument. Use --help to see all options.")

        if arg == 'update':
            print('Storing permissions and admin to file...')

            # Allows refreshing of stale initial group/permissions settings.
            with open('personal/fixtures/init_data.json', 'w') as output:
                call_command(
                    "dumpdata",
                    "auth",
                    "--exclude",
                    "auth.User",
                    "--natural-foreign",  # minimize conflicts with pks
                    "--natural-primary",  # even though should be new build
                    "--format=json",
                    "--indent",
                    "4",
                    stdout=output)

            # Try to export admin superuser directly.
            try:
                admin = User.objects.filter(
                    username="admin", is_superuser=True)
                serial_admin = serializers.serialize("json", admin)
                with open('personal/fixtures/init_superuser.json', 'w') as out:
                    out.write(serial_admin)
            except User.DoesNotExist:
                print("Admin does not exist.")

            print('Files updated.')

        elif arg == 'load':
            self.stdout.write('Adding default permissions and admin...')
            # Creates perms/groups
            call_command("loaddata", "init_data.json")
            # Creates superuser
            call_command("loaddata", "init_superuser.json")
            print("Created default groups and permissions.")
