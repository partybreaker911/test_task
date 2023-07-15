from django.views import View
from django.shortcuts import render

from apps.employee.service.employees import EmployeeService


class EmployeeListView(View):
    template_name = "employee/employee_list.html"
    service = EmployeeService()

    def get(self, request):
        employees = self.service._get_all_employee()

        context = {
            "employees": employees,
        }
        return render(request, self.template_name)
