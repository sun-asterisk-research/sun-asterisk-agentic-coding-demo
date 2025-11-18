"""
Django admin configuration for transactions app.

This module registers the Category and Transaction models with custom
admin configurations for better management interface.
"""

from django.contrib import admin
from transactions.models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.

    Displays category details with filtering and search capabilities.
    """

    list_display = ('icon', 'name', 'type', 'color')
    list_filter = ('type',)
    search_fields = ('name',)
    ordering = ('type', 'name')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Transaction model.

    Displays transaction details with filtering, search, and date hierarchy.
    """

    list_display = (
        'date', 'user', 'category', 'type', 'formatted_amount', 'note_preview'
    )
    list_filter = ('type', 'category', 'date', 'user')
    search_fields = ('user__username', 'user__email', 'note', 'category__name')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    list_per_page = 25
    list_select_related = ('user', 'category')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Transaction Information', {
            'fields': ('user', 'category', 'type', 'amount', 'date')
        }),
        ('Additional Details', {
            'fields': ('note',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def formatted_amount(self, obj):
        """Display formatted amount with currency."""
        return f"{obj.amount:,.0f} VND"
    formatted_amount.short_description = 'Amount'
    formatted_amount.admin_order_field = 'amount'

    def note_preview(self, obj):
        """Display truncated note preview."""
        if obj.note:
            return obj.note[:50] + '...' if len(obj.note) > 50 else obj.note
        return '-'
    note_preview.short_description = 'Note'
