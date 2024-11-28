# <project>/<app>/management/commands/seed_countries.py
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

# python manage.py seed --mode=refresh
from apps.users.models import User

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'
""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        self.run_seed(options['mode'])
        self.stdout.write('done.')

    def clear_data(self):
        """Deletes all the table data"""
        self.stdout.write('Deleting permissions...')
        Permission.objects.all().delete()

    def create_user(self):
        """Creates an address object combining different elements from the list"""
        self.stdout.write("Creating user")
        User.objects.create(
            password=make_password('password'),
            first_name='Admin',
            last_name='Admin',
            phone='79999999999',
            email='admin@1creator.ru',
            is_superuser=True,
            is_employee=True
        )

        self.stdout.write("User created")

    def run_seed(self, mode):
        """ Seed database based on mode

        :param mode: refresh / clear
        :return:
        """
        # Clear data from tables
        self.clear_data()
        if mode == MODE_CLEAR:
            return

        self.create_user()
