from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Load initial data from fixtures if DB is empty'

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Only load if no regular users exist (superuser might exist from auto-create)
        if User.objects.filter(is_superuser=False).count() == 0:
            fixtures_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')

            blog_fixture = os.path.join(fixtures_dir, 'blog_data.json')
            taggit_fixture = os.path.join(fixtures_dir, 'taggit_data.json')

            if os.path.exists(taggit_fixture):
                self.stdout.write('Loading taggit data...')
                call_command('loaddata', taggit_fixture)

            if os.path.exists(blog_fixture):
                self.stdout.write('Loading blog data...')
                call_command('loaddata', blog_fixture)

            self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS('Data already exists. Skipping.'))
