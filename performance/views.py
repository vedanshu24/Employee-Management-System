from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, Avg
from .models import Performance
from .serializers import PerformanceSerializer
from .filters import PerformanceFilter


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related('employee__user', 'employee__department')
    serializer_class = PerformanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PerformanceFilter
    search_fields = ['employee__user__first_name', 'employee__user__last_name', 'employee__employee_id', 'reviewed_by']
    ordering_fields = ['review_date', 'rating', 'created_at']
    ordering = ['-review_date', '-created_at']

    @action(detail=False, methods=['get'])
    @permission_classes([AllowAny])
    def rating_summary(self, request):
        rating_stats = Performance.objects.values('rating').annotate(count=Count('rating')).order_by('rating')
        return Response(rating_stats)

    @action(detail=False, methods=['get'])
    def department_performance(self, request):
        department = request.query_params.get('department')
        if not department:
            return Response({'error': 'department parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        performances = Performance.objects.filter(employee__department__name=department)
        avg_rating = performances.aggregate(avg_rating=Avg('rating'))
        rating_distribution = performances.values('rating').annotate(count=Count('rating'))
        
        return Response({
            'average_rating': avg_rating['avg_rating'],
            'rating_distribution': rating_distribution
        })

    @action(detail=False, methods=['get'])
    def employee_performance(self, request):
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response({'error': 'employee_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        performances = Performance.objects.filter(employee__employee_id=employee_id)
        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    @permission_classes([AllowAny])
    def statistics(self, request):
        total_performances = Performance.objects.count()
        avg_rating = Performance.objects.aggregate(avg_rating=Avg('rating'))
        rating_distribution = Performance.objects.values('rating').annotate(count=Count('rating'))
        
        return Response({
            'total_reviews': total_performances,
            'average_rating': avg_rating['avg_rating'],
            'rating_distribution': rating_distribution
        })
