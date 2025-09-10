from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'check_in_time', 'check_out_time']
    list_filter = ['status', 'date', 'employee__department']
    search_fields = ['employee__user__first_name', 'employee__user__last_name', 'employee__employee_id']
    raw_id_fields = ['employee']
