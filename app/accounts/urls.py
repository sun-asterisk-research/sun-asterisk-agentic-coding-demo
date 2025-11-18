"""URL configuration for accounts app."""

from django.urls import path
from accounts.views import (
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
    ProfileView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
