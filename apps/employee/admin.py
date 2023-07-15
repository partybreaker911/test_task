from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from apps.employee.models import Employee, Position


# class EmployeeMPTTModelAdmin(MPTTModelAdmin):
#     mtpp_level_ident = 20
#     # mptt_indent_field = "parent"
#     list_display = [
#         "tree_actions",
#         "indented_title",
#     ]


# admin.site.register(Employee, MPTTModelAdmin)
admin.site.register(
    Employee,
    DraggableMPTTAdmin,
    list_display=(
        "tree_actions",
        "indented_title",
        # ...more fields if you feel like it...
    ),
    list_display_links=("indented_title",),
)


class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "position_name",
    ]


admin.site.register(Position, PositionAdmin)
