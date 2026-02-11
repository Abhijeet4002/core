from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create a superuser if none exists (for automated deployments)'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists. Skipping.'))
