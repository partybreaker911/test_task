from django.urls import path

from apps.employee import views

app_name = "employee"

urlpatterns = [
    path("", views.EmployeeListView.as_view(), name="employee_list"),
    path("tree/", views.EmployeeTreeView.as_view(), name="employee_tree"),
    path("ajax_table/", views.EmployeeTableAjax.as_view(), name="employee_table_ajax"),
    path("<uuid:id>/detail", views.EmployeeEditView.as_view(), name="employee_detail"),
    path(
        "update_supervisor/",
        views.UpdateEmployeeSupervisor.as_view(),
        name="update_supervisor",
    ),
]
