from django.contrib import admin

from apps.employee.models import Employee, Position


class EmployeeInlineAdmin(admin.TabularInline):
    model = Employee
    list_display = [
        "full_name",
        "email",
        "position",
        "hire_date",
        "supervisor",
    ]


# admin.site.register(Employee, EmployeeAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "position_name",
    ]
    inlines = [
        EmployeeInlineAdmin,
    ]


admin.site.register(Position, PositionAdmin)
