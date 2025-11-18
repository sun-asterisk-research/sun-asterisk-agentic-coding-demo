"""Views for accounts app."""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from accounts.forms import UserRegistrationForm, UserProfileForm
from accounts.models import UserProfile


class RegisterView(CreateView):
    """
    View for user registration.

    Uses UserRegistrationForm to create new users with email and
    optional display_name. Auto-creates UserProfile via signal.
    Redirects to login page after successful registration.
    """

    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        """Redirect authenticated users away from registration page."""
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Handle successful form submission."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Đăng ký thành công! Vui lòng đăng nhập.'
        )
        return response


class CustomLoginView(LoginView):
    """
    Custom login view.

    Uses Django's built-in LoginView with custom template.
    """

    template_name = 'accounts/login.html'

    def get_success_url(self):
        """Redirect to next parameter or dashboard after login."""
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('dashboard')


class CustomLogoutView(LogoutView):
    """
    Custom logout view.

    Uses Django's built-in LogoutView with custom redirect.
    """

    next_page = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        """Add success message on logout."""
        if request.user.is_authenticated:
            messages.info(request, 'Bạn đã đăng xuất thành công.')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProfileView(UpdateView):
    """
    View for updating user profile.

    Allows authenticated users to update their display_name and
    monthly_budget. Only updates the current user's profile.
    """

    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        """Return the current user's profile."""
        return self.request.user.profile

    def get_initial(self):
        """Set initial form values from current user's profile."""
        initial = super().get_initial()
        profile = self.request.user.profile
        initial['display_name'] = profile.display_name
        initial['monthly_budget'] = profile.monthly_budget
        return initial

    def form_valid(self, form):
        """Handle successful form submission."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Hồ sơ của bạn đã được cập nhật thành công.'
        )
        return response
