from django.contrib import admin
from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'department', 'position', 'is_active', 'date_of_joining']
    list_filter = ['department', 'is_active', 'date_of_joining']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'user__email']
    raw_id_fields = ['user']
