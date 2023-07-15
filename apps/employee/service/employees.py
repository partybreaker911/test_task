from django.db.models import F

from apps.employee.models import Employee


class EmployeeService:
    @staticmethod
    def _get_all_employee():
        return Employee.objects.all()

    @staticmethod
    def _get_employee_data():
        employees = Employee.objects.select_related("parent").values(
            "id",
            "full_name",
            "position__position_name",
            "hire_date",
            "email",
            "supervisor__full_name",
        )
        data = list(employees)
        return data
