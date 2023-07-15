from typing import Any

from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from apps.employee.models import Employee


class Command(BaseCommand):
    """
    Command to delete all rows from the comm_employee table.
    """

    help = _("Delete all rows from the comm_employee table")

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Deletes all rows from the comm_employee table.
        """

        # Delete all records
        Employee.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                _("Successfully deleted all rows from the comm_employee table")
            )
        )
