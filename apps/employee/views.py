from typing import Any, Dict, Optional

from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    UpdateView,
    DeleteView,
    DetailView,
    CreateView,
)
from apps.employee.forms import EmployeeForm
from apps.employee.service.employees import Employee_service


class EmployeeListView(View):
    employee_service = Employee_service()
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
            self.employee_service._search_employees(search_query, self.items_per_page)
            if search_query
            else self.employee_service._get_paginated_employees(
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


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "employee/employee_edit.html"
    form_class = EmployeeForm
    employee_service = Employee_service()
    success_url = reverse_lazy("employee:employee_list")

    def get_object(self, queryset: Optional[QuerySet] = None) -> object:
        """
        Get the object using the provided queryset.

        Args:
            queryset (QuerySet, optional): The queryset to use for fetching the object. Defaults to None.

        Returns:
            object: The object fetched using the provided queryset.
        """
        return self.employee_service._get_employee_by_id(self.kwargs["employee_id"])


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "employee/employee_delete.html"
    employee_service = Employee_service()
    success_url = reverse_lazy("employee:employee_list")

    def delete(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        """
        Deletes an employee with the specified employee ID.

        Args:
            request (HttpRequest): The HTTP request object.
            args (list): Positional arguments.
            kwargs (dict): Keyword arguments.

        Returns:
            HttpResponse: If the employee is deleted successfully, returns the response from the super class's delete method.
                        If the employee is not found, returns an HttpResponse with a status code of 404.
        """
        employee_id = self.kwargs["employee_id"]
        result = self.employee_service._delete_employee(employee_id)

        if result:
            return super().delete(request, *args, **kwargs)
        else:
            return HttpResponse("Employee not found", status=404)

    def get_context_data(self, **kwargs) -> dict:
        """
        Retrieves the context data for the view.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        employee_id = self.kwargs["employee_id"]
        employee = self.employee_service._get_employee_by_id(employee_id)
        context["employee"] = employee
        return context

    def get_object(self, queryset: Optional[QuerySet] = None) -> None:
        """
        Get an object from the queryset.

        Args:
            queryset (QuerySet, optional): The queryset to retrieve the object from. Defaults to None.

        Returns:
            None: If the object is not found in the queryset.
        """
        if queryset is None:
            queryset = self.get_queryset()

        return None

    def get_queryset(self) -> QuerySet:
        """
        Retrieves the queryset for the current instance.

        :param self: The current instance.
        :return: The queryset for the current instance.
        :rtype: QuerySet
        """
        return self.employee_service._get_all_employees()


class EmployeeDetailView(DetailView):
    template_name = "employee/employee_detail.html"
    employee_service = Employee_service()
    pk_url_kwarg = "employee_id"

    def get_queryset(self) -> QuerySet:
        """
        Retrieve all employees from the employe_service.

        Returns:
            QuerySet: List of all employees.
        """
        return self.employee_service._get_all_employees()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Get the context data for the view.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data for the view.

        """
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        supervisors = self.employee_service._get_supervisors(employee.id)
        context["supervisors"] = supervisors
        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    template_name = "employee/employee_create.html"
    form_class = EmployeeForm
    employee_service = Employee_service()
    success_url = reverse_lazy("employee:employee_list")

    def form_valid(self, form) -> Any:
        """
        Save the form data to create a new employee.

        Args:
            form: An instance of the form containing the employee data.

        Returns:
            The result of calling the `form_valid` method of the parent class.
        """
        employee = form.save(commit=False)
        self.employee_service._create_employee(employee)
        return super().form_valid(form)
