"""Admin configuration for transactions app."""
from django.contrib import admin
from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model."""
    
    list_display = ['name', 'icon', 'transaction_type', 'color', 'created_at']
    list_filter = ['transaction_type']
    search_fields = ['name']
    ordering = ['transaction_type', 'name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin for Transaction model."""
    
    list_display = [
        'user', 'amount', 'transaction_type', 
        'category', 'date', 'created_at'
    ]
    list_filter = ['transaction_type', 'category', 'date']
    search_fields = ['user__username', 'note']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    raw_id_fields = ['user']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('user', 'amount', 'transaction_type', 'category', 'date')
        }),
        ('Thông tin bổ sung', {
            'fields': ('note',),
            'classes': ('collapse',)
        }),
    )
