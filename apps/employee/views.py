from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.employee.service.employees import EmployeeService


class EmployeeListView(View):
    template_name = "employee/employee_list.html"
    service = EmployeeService()

    def get(self, request):
        return render(request, self.template_name)


class EmployeeTableAjax(View):
    service = EmployeeService()

    def get(self, request):
        employees_data = self.service._get_employee_data()

        context = {
            "data": employees_data,
        }
        return JsonResponse(context)


class EmployeeTreeView(LoginRequiredMixin, View):
    template_name = "employee/employee_tree.html"
    service = EmployeeService()

    def get(self, request):
        return render(request, self.template_name)
