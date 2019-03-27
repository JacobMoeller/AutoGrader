"""
Creates permissions and groups automatically with custom command `chgroups`.
Loads fixtures stored in personal/fixtures for auth tables.

Used in manage.py to automate initial set-up with `add`. `update` allows
for automated storage in pre-defined filename/location to avoid inconsistency
from typo and provide minor ease of use in command length.

Superuser account is created with 'initial_accounts.json'; it cannot be updated
except by manual use of dumpdata.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Creates or updates default permission groups for groups.'

    # Allow user to specify `chgroups add`, as in first populating the database
    # with the user and admin models, or `chgroups update`, which updates the
    # fixtures which are loaded when the add command is executed.
    def add_arguments(self, parser):
        parser.add_argument(
          'action',
          type=str,
          help='Specify "add" to load permissions, "update" to store \
            any newly created groups or permissions.')

    def handle(self, *args, **kwargs):
        arg = kwargs['action']
        if arg == 'update':
            print('Storing permissions and admin to file...')

            # Allows refreshing of stale initial group/permissions settings.
            with open('personal/fixtures/initial_data.json', 'w') as output:
                call_command(
                    "dumpdata",
                    "--format=json",
                    "auth.group",
                    "auth.permission",
                    "auth.group_permissions",
                    stdout=output)
            print('Files updated.')

        elif arg == 'add':
            self.stdout.write('Adding default permissions and admin...')
            # Creates perms/groups
            call_command("loaddata", "initial_data.json")
            # Creates superuser
            call_command("loaddata", "initial_accounts.json")
            print("Created default groups and permissions.")
