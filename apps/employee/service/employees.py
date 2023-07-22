from uuid import uuid4
from typing import List
from datetime import datetime

from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from apps.employee.models import Employee


class EmployeeService:
    @staticmethod
    def _create_employee(employee) -> None:
        """
        Create a new employee.

        Parameters:
            employee (Employee): The employee object to create.

        Returns:
            None
        """
        employee.save()

    @staticmethod
    def _get_employee_by_id(employee_id: uuid4) -> Employee:
        """
        Retrieves a single employee based on the provided employee ID. If no such employee
        exists an Exception will be thrown.

        Args:
            employee_id: The ID of the requested Employee.

        Returns:
            Employee: The requested Employee.
        """
        try:
            employee = Employee.objects.get(pk=employee_id)
            return employee
        except Exception:
            raise ValueError(_("Employee not found"))

    @staticmethod
    def _get_all_employees() -> List[Employee]:
        """
        Retrieves all employees from the database.

        Returns:
            List[Employee]: A list of Employee objects representing all the employees.
        """
        return Employee.objects.all()

    @staticmethod
    def _get_supervisors(employee_id: int) -> List[Employee]:
        """
        Get the supervisors of an employee.

        Args:
            employee_id (int): The ID of the employee.

        Returns:
            List[Employee]: A list of supervisor employees.
        """
        employee = EmployeeService._get_employee_by_id(employee_id)
        supervisors = Employee.objects.filter(parent=employee).select_related(
            "position"
        )
        return supervisors

    @staticmethod
    def _search_employees(
        search_query: str, items_per_page: int = 15
    ) -> List[Employee]:
        """
        Search employees by the given query and paginate the results.

        Args:
            search_query: The query string to search for employees.
            items_per_page: The number of items per page (default: 15).

        Returns:
            A List object containing a subset of matching employees.
        """
        try:
            search_date = datetime.strptime(search_query, "%Y-%m-%d")
            employees = Employee.objects.filter(
                Q(full_name__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(position__icontains=search_query)
                | Q(parent__full_name__icontains=search_query)
                | Q(
                    hire_date__date__gte=search_date
                )  # Поиск даты больше или равной указанной
                | Q(
                    hire_date__date__lte=search_date
                )  # Поиск даты меньше или равной указанной
            )
        except ValueError:
            employees = Employee.objects.none()
        paginator = Paginator(employees, items_per_page)

        try:
            page = paginator.get_page(1)
        except EmptyPage:
            return None
        return page

    @staticmethod
    def _delete_employee(self, employee_id: int) -> bool:
        """
        Delete an employee with the given ID.

        Args:
            employee_id (int): The ID of the employee to delete.

        Returns:
            bool: True if the employee was successfully deleted, False otherwise.
        """
        try:
            employee = self._get_employee_by_id(employee_id)
            employee.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def _get_sorted_employees(sort_by: str) -> QuerySet:
        """
        Retrieves a sorted list of employees based on the provided sort field.

        Args:
            sort_by: The field to sort the employees by. Must be one of the following: "full_name",
                    "position", "hire_date", "email", "supervisor".

        Returns:
            QuerySet: A sorted QuerySet of Employee objects.
        """
        valid_sort_fields = [
            "full_name",
            "position",
            "hire_date",
            "email",
            "parent",
        ]
        if sort_by not in valid_sort_fields:
            sort_by = "parent"

        return Employee.objects.order_by(sort_by)

    @staticmethod
    def _get_paginated_employees(
        self, sort_by: str, page_number: int, items_per_page: int
    ) -> List:
        """
        Retrieves a paginated list of employees based on the given sorting criteria.

        Args:
            sort_by: The field to sort the employees by. Can be one of 'name', 'age', or 'salary'.
            page_number: The page number of the results to retrieve.
            items_per_page: The number of items to display per page.

        Returns:
            Page: A Page object containing the requested employees.
        """
        employees = self._get_sorted_employees(sort_by)

        paginator = Paginator(employees, items_per_page)
        page = paginator.get_page(page_number)

        return page
