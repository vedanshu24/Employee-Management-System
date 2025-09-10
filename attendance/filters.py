import django_filters
from .models import Attendance


class AttendanceFilter(django_filters.FilterSet):
    employee = django_filters.CharFilter(field_name='employee__employee_id')
    department = django_filters.CharFilter(field_name='employee__department__name')
    status = django_filters.ChoiceFilter(choices=Attendance.STATUS_CHOICES)
    date_after = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_before = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    year = django_filters.NumberFilter(field_name='date__year')
    month = django_filters.NumberFilter(field_name='date__month')

    class Meta:
        model = Attendance
        fields = ['employee', 'status', 'date']
