"""Views for accounts app."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm


def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto login after registration
            login(request, user)
            messages.success(
                request,
                f'Chào mừng {user.username}! Tài khoản đã được tạo thành công.'
            )
            return redirect('dashboard')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """Profile view - placeholder."""
    return render(request, 'accounts/profile.html')
