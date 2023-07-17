from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from apps.employee.models import Employee, Position


class EmployeeMPTTModelAdmin(DraggableMPTTAdmin):
    expand_tree_by_default = True


admin.site.register(Employee, EmployeeMPTTModelAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "position_name",
    ]


admin.site.register(Position, PositionAdmin)
