from rest_framework import serializers
from .models import Performance
from employees.serializers import EmployeeSerializer


class PerformanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    rating_display = serializers.ReadOnlyField()

    class Meta:
        model = Performance
        fields = [
            'id', 'employee', 'employee_name', 'employee_id', 'department_name',
            'rating', 'rating_display', 'review_date', 'goals_achieved',
            'areas_for_improvement', 'comments', 'reviewed_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
