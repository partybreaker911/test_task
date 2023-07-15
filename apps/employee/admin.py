from django.contrib import admin

from apps.employee.models import Employee, Position


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "email",
        "position",
        "hire_date",
        "supervisor",
    ]


admin.site.register(Employee, EmployeeAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "position_name",
    ]


admin.site.register(Position, PositionAdmin)
