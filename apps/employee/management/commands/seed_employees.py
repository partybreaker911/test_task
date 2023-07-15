import random
from uuid import uuid4
from django.core.management.base import BaseCommand
from faker import Faker
from apps.employee.models import Employee, Position

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with employee data"

    def add_arguments(self, parser):
        parser.add_argument(
            "num_employees", type=int, help="Number of employees to generate"
        )
        parser.add_argument("num_levels", type=int, help="Number of hierarchy levels")

    def create_positions(self, num_positions):
        positions = []

        for _ in range(num_positions):
            position_name = fake.job()
            position = Position.objects.create(position_name=position_name)
            positions.append(position)

        Position.objects.bulk_create(positions)

    def handle(self, *args, **options):
        num_employees = options["num_employees"]
        num_levels = options["num_levels"]

        self.create_positions(num_levels)

        # Генерация начальника
        boss_position = Position.objects.first()
        boss = Employee.objects.create(
            id=uuid4(),
            full_name=fake.name(),
            position=boss_position,
            hire_date=fake.date_between(start_date="-5y", end_date="today"),
            email=fake.email(),
            supervisor=None,
            show_supervisors=True,
        )

        # Генерация остальных сотрудников
        for _ in range(num_employees - 1):
            parent = random.choice(Employee.objects.all())
            employee_position = random.choice(Position.objects.all())
            employee = Employee.objects.create(
                id=uuid4(),
                full_name=fake.name(),
                position=employee_position,
                hire_date=fake.date_between(start_date="-5y", end_date="today"),
                email=fake.email(),
                supervisor=parent,
                show_supervisors=True,
            )

        # Обновление уровней иерархии
        Employee.objects.rebuild()

        # Генерация дополнительных уровней иерархии
        for level in range(2, num_levels + 1):
            employees = Employee.objects.filter(level=level - 1)
            for employee in employees:
                for _ in range(random.randint(1, 5)):
                    subordinate_position = random.choice(Position.objects.all())
                    subordinate = Employee.objects.create(
                        id=uuid4(),
                        full_name=fake.name(),
                        position=subordinate_position,
                        hire_date=fake.date_between(start_date="-5y", end_date="today"),
                        email=fake.email(),
                        supervisor=employee,
                        show_supervisors=True,
                    )

        self.stdout.write(
            self.style.SUCCESS("Database seeding completed successfully.")
        )
