from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, EmployeeViewSet, charts_view, PublicStatisticsView

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('charts/', charts_view, name='charts'),
    path('public-stats/', PublicStatisticsView.as_view(), name='public-stats'),
]
