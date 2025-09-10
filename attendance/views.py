from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import Attendance
from .serializers import AttendanceSerializer, AttendanceCreateSerializer
from .filters import AttendanceFilter


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('employee__user', 'employee__department')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AttendanceFilter
    search_fields = ['employee__user__first_name', 'employee__user__last_name', 'employee__employee_id']
    ordering_fields = ['date', 'created_at', 'employee__user__first_name']
    ordering = ['-date', '-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return AttendanceCreateSerializer
        return AttendanceSerializer

    @action(detail=False, methods=['get'])
    @permission_classes([AllowAny])
    def monthly_summary(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        if not month or not year:
            return Response({'error': 'Month and year parameters are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response({'error': 'Invalid month or year format'}, status=status.HTTP_400_BAD_REQUEST)
        
        attendances = Attendance.objects.filter(
            date__year=year,
            date__month=month
        ).values('status').annotate(count=Count('status'))
        
        return Response(attendances)

    @action(detail=False, methods=['get'])
    def employee_attendance(self, request):
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response({'error': 'employee_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        attendances = Attendance.objects.filter(employee__employee_id=employee_id)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    @permission_classes([AllowAny])
    def statistics(self, request):
        total_attendance = Attendance.objects.count()
        present_count = Attendance.objects.filter(status='present').count()
        absent_count = Attendance.objects.filter(status='absent').count()
        late_count = Attendance.objects.filter(status='late').count()
        
        return Response({
            'total_records': total_attendance,
            'present': present_count,
            'absent': absent_count,
            'late': late_count,
            'attendance_rate': (present_count / total_attendance * 100) if total_attendance > 0 else 0
        })
