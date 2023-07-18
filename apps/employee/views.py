from typing import Any, Dict, Optional

from django.db import models
from django.urls import reverse_lazy
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
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
    service = EmployeeService()
    success_url = reverse_lazy("employee:employee_list")

    def get_object(self, queryset: Optional[QuerySet] = None) -> object:
        """
        Get the object using the provided queryset.

        Args:
            queryset (QuerySet, optional): The queryset to use for fetching the object. Defaults to None.

        Returns:
            object: The object fetched using the provided queryset.
        """
        return self.service._get_employee_by_id(self.kwargs["employee_id"])


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "employee/employee_delete.html"
    service = EmployeeService()
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
        result = self.service._delete_employee(employee_id)

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
        employee = self.service._get_employee_by_id(employee_id)
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
        return self.service._get_all_employees()


class EmployeeDetailView(DetailView):
    template_name = "employee/employee_detail.html"
    service = EmployeeService()
    pk_url_kwarg = "employee_id"

    def get_queryset(self) -> QuerySet:
        """
        Retrieve all employees from the service.

        Returns:
            QuerySet: List of all employees.
        """
        return self.service._get_all_employees()

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
        supervisors = self.service._get_supervisors(employee.id)
        context["supervisors"] = supervisors
        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    template_name = "employee/employee_create.html"
    form_class = EmployeeForm
    service = EmployeeService()
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
        self.service._create_employee(employee)
        return super().form_valid(form)


# class EmployeeListView(View):
#     template_name = "employee/employee_list.html"
#     service = EmployeeService()

#     def get(self, request: HttpRequest) -> HttpResponse:
#         """Handles the HTTP GET request.

#         Args:
#             request: The HTTP request object.

#         Returns:
#             The rendered HTML response.
#         """
#         return render(request, self.template_name)


# class EmployeeTableAjax(View):
#     service = EmployeeService()

#     def get(self, request: HttpRequest) -> JsonResponse:
#         """Retrieve employee data.

#         Args:
#             request: The HTTP request object.

#         Returns:
#             JsonResponse: The JSON response containing the employee data.
#         """
#         employees_data = self.service._get_employee_data()

#         context = {
#             "data": employees_data,
#         }

#         return JsonResponse(context)


# class EmployeeEditView(LoginRequiredMixin, UpdateView):
#     template_name = "employee/employee_edit.html"
#     form_class = EmployeeForm
#     service = EmployeeService()

#     def get_object(self, queryset=None):
#         return self.service._get_employee_by_id(self.kwargs["id"])


# class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
#     template_name = "employee/employee_delete.html"
#     service = EmployeeService()

#     def delete(self, request: HttpRequest, *args, **kwargs):
#         """
#         Delete an employee.

#         Args:
#             request (HttpRequest): The HTTP request object.
#             *args: Variable length argument list.
#             **kwargs: Arbitrary keyword arguments.

#         Returns:
#             The result of deleting the employee.
#         """
#         return self.service._delete_employee(self.get_object())


# class EmployeeTreeView(LoginRequiredMixin, View):
#     template_name = "employee/employee_tree.html"
#     service = EmployeeService()

#     def get(self, request: HttpRequest) -> HttpResponse:
#         """Get the top-level employees and their respective subordinates.

#         Args:
#             request: The request object.

#         Returns:
#             The rendered response containing the employees and their subordinates.
#         """

#         top_level_employees = self.service._get_top_level_employee()
#         employees = [
#             self.service._get_employee_with_depth(e) for e in top_level_employees
#         ]

#         context = {
#             "employees": employees,
#         }
#         return render(request, self.template_name, context)


# class UpdateEmployeeSupervisor(View):
#     service = EmployeeService()

#     def post(self, request: HttpRequest) -> JsonResponse:
#         """
#         Handles the POST request for updating the supervisor of an employee.

#         Args:
#             request: The HTTP request object containing the employee_id and supervisor_id.

#         Returns:
#             The JSON response object containing the success status and message.
#         """
#         employee_id = request.POST.get("employee_id")
#         supervisor_id = request.POST.get("supervisor_id")

#         try:
#             self.service._update_supervisor(employee_id, supervisor_id)
#             response_data = {
#                 "success": True,
#                 "message": _("Successfully updated supervisor"),
#             }
#         except self.service.EmployeeNotFoundError:
#             response_data = {
#                 "success": False,
#                 "message": _("Employee or new supervisor not found."),
#             }
#         except Exception as e:
#             response_data = {
#                 "success": False,
#                 "message": str(e),
#             }
#         return JsonResponse(response_data)
