from django.contrib import admin
from .models import Performance


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'rating', 'review_date', 'reviewed_by']
    list_filter = ['rating', 'review_date', 'employee__department']
    search_fields = ['employee__user__first_name', 'employee__user__last_name', 'employee__employee_id', 'reviewed_by']
    raw_id_fields = ['employee']
