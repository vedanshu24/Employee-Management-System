from rest_framework import serializers
from .models import Attendance
from employees.serializers import EmployeeSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    working_hours = serializers.ReadOnlyField()

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'employee_id', 'department_name',
            'date', 'status', 'check_in_time', 'check_out_time', 'working_hours',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            'employee', 'date', 'status', 'check_in_time', 'check_out_time', 'notes'
        ]

    def validate(self, data):
        if data.get('check_in_time') and data.get('check_out_time'):
            if data['check_in_time'] >= data['check_out_time']:
                raise serializers.ValidationError("Check-out time must be after check-in time.")
        return data
