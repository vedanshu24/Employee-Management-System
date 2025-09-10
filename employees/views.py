from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer, EmployeeCreateSerializer
from .filters import EmployeeFilter


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        department = self.get_object()
        employees = department.employees.filter(is_active=True)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.filter(is_active=True).select_related('user', 'department')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EmployeeFilter
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'employee_id', 'position']
    ordering_fields = ['date_of_joining', 'created_at', 'user__first_name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeCreateSerializer
        return EmployeeSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['get'])
    def attendance_summary(self, request, pk=None):
        employee = self.get_object()
        from attendance.models import Attendance
        from django.db.models import Count
        
        attendance_stats = Attendance.objects.filter(employee=employee).values('status').annotate(count=Count('status'))
        return Response(attendance_stats)

    @action(detail=True, methods=['get'])
    def performance_summary(self, request, pk=None):
        employee = self.get_object()
        from performance.models import Performance
        from django.db.models import Avg
        
        avg_rating = Performance.objects.filter(employee=employee).aggregate(avg_rating=Avg('rating'))
        latest_performance = Performance.objects.filter(employee=employee).first()
        
        return Response({
            'average_rating': avg_rating['avg_rating'],
            'latest_performance': PerformanceSerializer(latest_performance).data if latest_performance else None
        })

    @action(detail=False, methods=['get'])
    @permission_classes([AllowAny])
    def statistics(self, request):
        total_employees = Employee.objects.filter(is_active=True).count()
        department_stats = Department.objects.annotate(employee_count=Count('employees', filter=Q(employees__is_active=True)))
        
        return Response({
            'total_employees': total_employees,
            'departments': DepartmentSerializer(department_stats, many=True).data
        })


from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

@require_http_methods(["GET"])
def charts_view(request):
    return render(request, 'charts.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class PublicStatisticsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        from attendance.models import Attendance
        from performance.models import Performance
        from django.db.models import Avg
        
        # Employee statistics
        total_employees = Employee.objects.filter(is_active=True).count()
        department_stats = Department.objects.annotate(employee_count=Count('employees', filter=Q(employees__is_active=True)))
        
        # Attendance statistics
        total_attendance = Attendance.objects.count()
        present_count = Attendance.objects.filter(status='present').count()
        absent_count = Attendance.objects.filter(status='absent').count()
        late_count = Attendance.objects.filter(status='late').count()
        
        # Performance statistics
        total_performances = Performance.objects.count()
        avg_rating = Performance.objects.aggregate(avg_rating=Avg('rating'))
        
        # Monthly attendance summary (current month)
        from datetime import datetime
        current_date = datetime.now()
        monthly_attendance = Attendance.objects.filter(
            date__year=current_date.year,
            date__month=current_date.month
        ).values('status').annotate(count=Count('status'))
        
        # Performance rating distribution
        rating_distribution = Performance.objects.values('rating').annotate(count=Count('rating')).order_by('rating')
        
        return Response({
            'employees': {
                'total_employees': total_employees,
                'departments': DepartmentSerializer(department_stats, many=True).data
            },
            'attendance': {
                'total_records': total_attendance,
                'present': present_count,
                'absent': absent_count,
                'late': late_count,
                'attendance_rate': (present_count / total_attendance * 100) if total_attendance > 0 else 0,
                'monthly_summary': list(monthly_attendance)
            },
            'performance': {
                'total_reviews': total_performances,
                'average_rating': avg_rating['avg_rating'],
                'rating_distribution': list(rating_distribution)
            }
        })