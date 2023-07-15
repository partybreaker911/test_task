from django import forms

from apps.employee.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "full_name",
            "email",
            "position",
            "parent",
            "hire_date",
        ]
