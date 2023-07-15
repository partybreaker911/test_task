from django.views.generic import View
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.employee.forms import EmployeeForm
from apps.employee.service.employees import EmployeeService


class EmployeeListView(View):
    template_name = "employee/employee_list.html"
    service = EmployeeService()

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handles the HTTP GET request.

        Args:
            request: The HTTP request object.

        Returns:
            The rendered HTML response.
        """
        return render(request, self.template_name)


class EmployeeTableAjax(View):
    service = EmployeeService()

    def get(self, request: HttpRequest) -> JsonResponse:
        """Retrieve employee data.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: The JSON response containing the employee data.
        """
        employees_data = self.service._get_employee_data()

        context = {
            "data": employees_data,
        }

        return JsonResponse(context)


class EmployeeEditView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: dict) -> HttpResponse:
        """
        Get method to retrieve an employee's information by their ID.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - kwargs (dict): Additional keyword arguments.
            - id (int): The ID of the employee.

        Returns:
        - HttpResponse: The rendered template with the employee's information.
        """
        employee_id: int = kwargs["id"]
        employee = self.service._get_employee_by_id(employee_id)

        form = EmployeeForm(instance=employee)

        context = {
            "form": form,
        }

        return render(request, self.template_name, context)

    def post(request: HttpRequest, **kwargs: dict) -> HttpResponse:
        """
        Handle the HTTP POST request for updating an employee.

        Args:
            request: The HTTP request object.
            **kwargs: Additional keyword arguments.

        Returns:
            The HTTP response object.
        """
        employee_id = kwargs["id"]
        data = request.POST

        service = EmployeeService()
        if service.update_employee(employee_id, data):
            return redirect("employee:employee_list")
        else:
            form = EmployeeForm(data)
            context = {
                "form": form,
            }
            return render(request, "template_name", context)


class EmployeeTreeView(LoginRequiredMixin, View):
    template_name = "employee/employee_tree.html"
    service = EmployeeService()

    def get(self, request: HttpRequest) -> HttpResponse:
        """Get the top-level employees and their respective subordinates.

        Args:
            request: The request object.

        Returns:
            The rendered response containing the employees and their subordinates.
        """
        top_level_employees = self.service._get_top_level_employee()
        employees = [
            self.service._get_employee_with_depth(e) for e in top_level_employees
        ]

        context = {
            "employees": employees,
        }
        return render(request, self.template_name, context)


class UpdateEmployeeSupervisor(View):
    service = EmployeeService()

    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Handles the POST request for updating the supervisor of an employee.

        Args:
            request: The HTTP request object containing the employee_id and supervisor_id.

        Returns:
            The JSON response object containing the success status and message.
        """
        employee_id = request.POST.get("employee_id")
        supervisor_id = request.POST.get("supervisor_id")

        try:
            self.service._update_supervisor(employee_id, supervisor_id)
            response_data = {
                "success": True,
                "message": _("Successfully updated supervisor"),
            }
        except self.service.EmployeeNotFoundError:
            response_data = {
                "success": False,
                "message": _("Employee or new supervisor not found."),
            }
        except Exception as e:
            response_data = {
                "success": False,
                "message": str(e),
            }
        return JsonResponse(response_data)
