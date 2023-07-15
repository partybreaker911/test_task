from apps.employee.models import Employee


class EmployeeService:
    @staticmethod
    def _get_all_employee():
        return Employee.objects.all()
