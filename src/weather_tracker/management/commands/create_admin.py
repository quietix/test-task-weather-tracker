from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings


class Command(BaseCommand):
    help = "Create an admin user with credentials from .env"

    def handle(self, *args, **options):
        User = get_user_model()

        username = settings.ADMIN_USERNAME
        password = settings.ADMIN_PASSWORD

        if not password:
            self.stderr.write(self.style.ERROR("ADMIN_PASSWORD is not set in settings.py"))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.NOTICE(f"Admin user '{username}' already exists."))
        else:
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f"Admin user '{username}' created."))
