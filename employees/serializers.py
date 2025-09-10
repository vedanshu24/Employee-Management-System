from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    employees_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'employees_count']

    def get_employees_count(self, obj):
        return obj.employees.filter(is_active=True).count()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active']


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'employee_id', 'phone', 'address', 'date_of_joining',
            'department', 'department_name', 'position', 'salary', 'is_active',
            'created_at', 'updated_at', 'full_name', 'email'
        ]
        read_only_fields = ['employee_id', 'created_at', 'updated_at']


class EmployeeCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Employee
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'phone', 'address', 'date_of_joining', 'department', 'position', 'salary'
        ]

    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'email': validated_data.pop('email'),
        }
        
        user = User.objects.create_user(**user_data)
        
        employee_id = f"EMP{user.id:04d}"
        validated_data['employee_id'] = employee_id
        validated_data['user'] = user
        
        return Employee.objects.create(**validated_data)
