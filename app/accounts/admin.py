"""
Django admin configuration for accounts app.

This module registers the UserProfile model with custom admin configuration
for better management interface.
"""

from django.contrib import admin
from accounts.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.

    Displays user profile details with search capabilities.
    """

    list_display = (
        'user', 'display_name', 'formatted_budget', 'user_email', 'date_joined'
    )
    search_fields = ('user__username', 'user__email', 'display_name')
    list_filter = ('user__date_joined', 'user__is_active')
    list_per_page = 25
    list_select_related = ('user',)
    readonly_fields = ('user_date_joined',)
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('display_name', 'monthly_budget')
        }),
        ('User Details', {
            'fields': ('user_date_joined',),
            'classes': ('collapse',)
        }),
    )

    def formatted_budget(self, obj):
        """Display formatted budget with currency."""
        if obj.monthly_budget:
            return f"{obj.monthly_budget:,.0f} VND"
        return 'Not set'
    formatted_budget.short_description = 'Monthly Budget'
    formatted_budget.admin_order_field = 'monthly_budget'

    def user_email(self, obj):
        """Display user email."""
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def date_joined(self, obj):
        """Display user registration date."""
        return obj.user.date_joined.strftime('%Y-%m-%d %H:%M')
    date_joined.short_description = 'Date Joined'
    date_joined.admin_order_field = 'user__date_joined'

    def user_date_joined(self, obj):
        """Display full user registration datetime."""
        return obj.user.date_joined
    user_date_joined.short_description = 'Date Joined'
