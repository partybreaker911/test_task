from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.employee.service.employees import EmployeeService


class EmployeeListView(View):
    template_name = "employee/employee_list.html"
    service = EmployeeService()

    def get(self, request):
        """
        Get method that handles the HTTP GET request.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered HTML response.
        """
        return render(request, self.template_name)


class EmployeeTableAjax(View):
    service = EmployeeService()

    def get(self, request):
        """
        Get method to retrieve employee data.

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


class EmployeeTreeView(LoginRequiredMixin, View):
    template_name = "employee/employee_tree.html"
    service = EmployeeService()

    def get(self, request):
        """
        Get the top-level employees and their respective subordinates.

        Parameters:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The rendered response containing the employees and their subordinates.
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

    def post(self, request):
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

        # employee = self.service._get_employee_and_supervisor_by_id(employee_id)
