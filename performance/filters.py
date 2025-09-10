import django_filters
from .models import Performance


class PerformanceFilter(django_filters.FilterSet):
    employee = django_filters.CharFilter(field_name='employee__employee_id')
    department = django_filters.CharFilter(field_name='employee__department__name')
    rating = django_filters.NumberFilter(field_name='rating')
    rating_min = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_max = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')
    review_date_after = django_filters.DateFilter(field_name='review_date', lookup_expr='gte')
    review_date_before = django_filters.DateFilter(field_name='review_date', lookup_expr='lte')
    reviewed_by = django_filters.CharFilter(field_name='reviewed_by', lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='review_date__year')

    class Meta:
        model = Performance
        fields = ['employee', 'rating', 'reviewed_by']
