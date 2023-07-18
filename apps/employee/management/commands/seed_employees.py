import json
import random
import sys
from uuid import uuid4
from faker import Faker

from django.core.management.base import BaseCommand

from apps.employee.models import Position, Employee


faker = Faker()

positions_list = [
    "CEO",
    "Team Lead",
    "Employee",
    "Intern",
    "Data Analyst",
    "Mechanical engineer",
    "HR",
    "UI Developer",
    "UI/UX",
    "Backend Architect",
    "Frontend Architect",
    "Software Tester",
    "QA",
]


class Command(BaseCommand):
    help = "Create json file with fake employees for future load in DB"

    def add_arguments(self, parser):
        parser.add_argument("employees", type=int)
        parser.add_argument("supervisors", type=int)

    @staticmethod
    def print_success_message(number_of_employees):
        print(
            f"\033[92m  Creation of {number_of_employees} employees was successful!\033[0m"
        )

    @staticmethod
    def create_positions(data):
        for i, position_name in enumerate(positions_list):
            position = Position.objects.create(position_name=position_name)
            position_record = {
                "model": "employee.position",
                "pk": str(position.id),
                "fields": {
                    "position_name": position.position_name,
                },
            }
            data.append(position_record)
        return data

    @staticmethod
    def write_to_json(data):
        with open("apps/employee/fixtures/employee_data.json", "w") as json_file:
            json.dump(data, json_file, indent=4, separators=(",", ": "))

    @staticmethod
    def create_employees(number_of_employees, number_of_supervisors, data):
        employees = []

        # Создаем начальника высшего уровня
        root_manager = None
        if number_of_supervisors > 0:
            full_name = faker.name()
            email = faker.email()
            hired = faker.date_between(start_date="-5y", end_date="today").strftime(
                "%Y-%m-%d"
            )
            position = random.choice(Position.objects.all())

            root_manager = Employee.objects.create(
                id=uuid4(),
                full_name=full_name,
                email=email,
                hire_date=hired,
                position=position,
                show_supervisors=True,
            )

            employees.append(root_manager)

        # Создаем подчиненных
        for _ in range(number_of_employees - number_of_supervisors):
            full_name = faker.name()
            email = faker.email()
            hired = faker.date_between(start_date="-5y", end_date="today").strftime(
                "%Y-%m-%d"
            )
            position = random.choice(Position.objects.all())

            # Выбираем случайного начальника из уже созданных сотрудников
            parent = random.choice(employees)

            employee = Employee.objects.create(
                id=uuid4(),
                full_name=full_name,
                email=email,
                hire_date=hired,
                position=position,
                show_supervisors=True,
                parent=parent,
            )

            employees.append(employee)

        # Добавляем записи в JSON
        for employee in employees:
            record = {
                "model": "employee.employee",
                "pk": str(employee.id),
                "fields": {
                    "full_name": employee.full_name,
                    "email": employee.email,
                    "hire_date": str(employee.hire_date),
                    "position": str(employee.position_id),
                    "parent": str(employee.parent_id) if employee.parent else None,
                    "show_supervisors": employee.show_supervisors,
                },
            }
            data.append(record)

        return data

    def handle(self, *args, **options):
        data = []

        if not options["employees"]:
            if len(sys.argv) != 3:
                print(
                    "\n  Usage: python db_seeder.py <number_of_employees> <number_of_supervisors>"
                )
                sys.exit()
            number_of_employees = int(sys.argv[1])
            number_of_supervisors = int(sys.argv[2])

        else:
            number_of_employees = options["employees"]
            number_of_supervisors = options["supervisors"]
            print(
                f"\n\033[93m  Usage: python manage.py db_seeder {number_of_employees} {number_of_supervisors}\033[0m"
            )

        data = self.create_positions(data)
        data = self.create_employees(number_of_employees, number_of_supervisors, data)
        self.write_to_json(data)
        self.print_success_message(number_of_employees)
