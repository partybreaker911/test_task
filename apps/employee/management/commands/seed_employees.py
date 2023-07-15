from faker import Faker
from random import randint
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from apps.employee.models import Position, Employee


class Command(BaseCommand):
    help = "Generate fake data for employees"

    def handle(self, *args, **options):
        fake = Faker()

        # Создание должностей
        positions = []
        for _ in range(7):
            position_name = fake.job()
            position = Position(position_name=position_name)
            positions.append(position)
        Position.objects.bulk_create(positions)

        # Генерация данных для сотрудников
        employees = []
        for _ in range(50000):
            full_name = fake.name()
            position = Position.objects.order_by("?").first()
            hire_date = fake.date_between(start_date="-10y", end_date="today")
            email = fake.email()

            employee = Employee(
                full_name=full_name,
                position=position,
                hire_date=hire_date,
                email=email,
            )
            employees.append(employee)

        Employee.objects.bulk_create(employees)

        # Назначение руководителей
        employees = Employee.objects.all()
        for employee in employees:
            employee.supervisor = (
                Employee.objects.exclude(id=employee.id).order_by("?").first()
            )
            employee.save()

        self.stdout.write(self.style.SUCCESS("Fake data generation completed!"))
