import random
from faker import Faker

from django.utils import timezone
from django.core.management.base import BaseCommand


from apps.employee.models import Position, Employee


class Command(BaseCommand):
    help = "Seed the database with fake data"

    def handle(self, *args, **options):
        fake = Faker()
        parent = None
        positions = []

        # Создание должностей
        for i in range(7):
            position = Position.objects.create(position_name=fake.job())
            positions.append(position)

        # Создание главного шефа
        boss = Employee.objects.create(
            full_name=fake.name(),
            position=random.choice(positions),
            hire_date=timezone.now().date(),
            email=fake.email(),
            parent=parent,
            show_supervisors=True,
        )
        parent = boss

        # Создание остальных сотрудников
        for _ in range(49999):
            employee = Employee.objects.create(
                full_name=fake.name(),
                position=random.choice(positions),
                hire_date=fake.past_date(),
                email=fake.email(),
                parent=parent,
                show_supervisors=True,
            )
            parent = employee

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
