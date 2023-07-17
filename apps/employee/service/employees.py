import uuid
from typing import List, Dict

from django.db.models import F, QuerySet

from apps.employee.models import Employee
from apps.employee.forms import EmployeeForm


class EmployeeService:
    """
    Employee service class thats contains business logic for the employees
    """

    @staticmethod
    def _get_employee_by_id(employee_id: uuid) -> Employee:
        """
        Get an employee by ID.
        """
        return Employee.objects.get(id=employee_id)

    @staticmethod
    def _update_employee(employee_id: uuid, new_data: dict) -> None:
        """
        Updates an employee's data.

        :param employee_id: The ID of the employee to update.
        :param new_data: The new employee data to update.
        """
        employee = EmployeeService._get_employee_by_id(employee_id)
        form = EmployeeForm(instance=employee, data=new_data)
        if form.is_valid():
            form.save()
            return True
        return False

    @staticmethod
    def _update_supervisor(employee_id: uuid, new_supervisor_id: uuid) -> None:
        """
        Updates the supervisor ID of an employee.

        :param employee_id: The ID of the employee to be updated.
        :param new_supervisor_id: The ID of the new supervisor.
        """
        Employee.objects.filter(id=employee_id).update(supervisor_id=new_supervisor_id)

    @staticmethod
    def _get_employee_data() -> List[Dict[str, object]]:
        """
        Get employee data from the database.

        Returns:
            list: A list of dictionaries containing employee data. Each dictionary contains the following keys:
                - id (int): The employee's ID.
                - full_name (str): The employee's full name.
                - position__position_name (str): The name of the employee's position.
                - hire_date (date): The date the employee was hired.
                - email (str): The employee's email address.
                - supervisor__full_name (str): The full name of the employee's supervisor.
        """
        employees = Employee.objects.select_related("parent").values(
            "id",
            "full_name",
            "position__position_name",
            "hire_date",
            "email",
            "parent__full_name",
        )
        data = list(employees)
        return data

    @staticmethod
    def _get_employee_with_depth(employee, depth=0):
        """
        Returns a dictionary containing information about the given employee and their supervisors up to a certain depth.

        Parameters:
        - employee: The employee object for which to retrieve information.
        - depth (optional): The depth up to which to retrieve supervisor information. Defaults to 0.

        Returns:
        A dictionary with the following keys:
        - "employee": The given employee object.
        - "depth": The depth of the employee in the supervisor hierarchy.
        - "show_supervisors": A boolean indicating whether to include supervisor information for the employee.
        - "supervisors": A list of dictionaries, each containing information about a supervisor of the employee up to the specified depth.
        """
        return {
            "employee": employee,
            "depth": depth,
            "show_supervisors": employee.show_supervisors,
            "supervisors": [
                EmployeeService._get_employee_with_depth(e, depth + 1)
                for e in employee.children.all()
                if employee.show_supervisors
            ],
        }

    @staticmethod
    def _get_top_level_employee() -> QuerySet[Employee]:
        """
        Retrieves the top level employee(s) from the database.

        :return: A QuerySet of Employee objects representing the top level employee(s).
        """
        return Employee.objects.filter(supervisor__isnull=True)
