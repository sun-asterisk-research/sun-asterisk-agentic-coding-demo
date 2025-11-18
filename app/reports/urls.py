"""URL configuration for reports app."""

from django.urls import path
from .views import DashboardView, ReportsView, ChartDataAPIView

app_name = 'reports'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', ReportsView.as_view(), name='reports'),
    path('api/chart-data/', ChartDataAPIView.as_view(), name='chart-data'),
]
