import django_filters
from .models import Employee, Department


class EmployeeFilter(django_filters.FilterSet):
    department = django_filters.ModelChoiceFilter(queryset=Department.objects.all())
    date_of_joining_after = django_filters.DateFilter(field_name='date_of_joining', lookup_expr='gte')
    date_of_joining_before = django_filters.DateFilter(field_name='date_of_joining', lookup_expr='lte')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    position = django_filters.CharFilter(field_name='position', lookup_expr='icontains')
    salary_min = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary', lookup_expr='lte')

    class Meta:
        model = Employee
        fields = ['department', 'is_active', 'position']
