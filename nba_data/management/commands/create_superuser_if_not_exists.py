from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

            if not (username and email and password):
                self.stdout.write(self.style.ERROR('Superuser environment variables are not set'))
                return

            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
