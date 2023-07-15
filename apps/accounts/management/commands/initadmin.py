from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from typing import Any

User = get_user_model()


class Command(BaseCommand):
    help = "Creates an initial admin user."

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Handle command execution.

        Args:
            *args: positional arguments.
            **options: keyword arguments.

        Returns:
            None.
        """
        username = "admin"
        email = "admin@example.com"
        password = "admin"

        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS("Initial admin user created."))
        else:
            self.stdout.write(self.style.WARNING("Initial admin user already exists."))
