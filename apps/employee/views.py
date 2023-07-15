from django.views import View
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _

from apps.employee.service.employees import EmployeeService


class EmployeeListView(View):
    employee_service = EmployeeService()
    template_name = "employee/employee_list.html"
    items_per_page = 15

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Retrieves a paginated list of employees based on the provided parameters.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template.
        """
        sort_by = request.GET.get("sort_by", "first_name")
        page_number = int(request.GET.get("page", 1))
        search_query = request.GET.get("search", "").strip()

        employees = (
            self.employee_service.search_employees(search_query, self.items_per_page)
            if search_query
            else self.employee_service.get_paginated_employees(
                sort_by, page_number, self.items_per_page
            )
        )

        context = {
            "employees": employees,
            "has_previous": employees.has_previous(),
            "has_next": employees.has_next(),
            "previous_page_number": employees.previous_page_number()
            if employees.has_previous()
            else None,
            "next_page_number": employees.next_page_number()
            if employees.has_next()
            else None,
        }

        return render(request, self.template_name, context)
