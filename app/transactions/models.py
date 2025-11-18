"""
Models for the transactions app.

This module contains the Category and Transaction models for tracking
financial transactions in the personal finance application.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """
    Category model for organizing transactions.

    Attributes:
        name: The name of the category (max 100 characters)
        icon: Emoji icon for visual representation (max 10 characters)
        type: Type of category (income or expense)
        color: Hex color code for UI display (max 7 characters)
        created_at: Timestamp when category was created
    """

    TYPE_CHOICES = [
        ('income', 'Thu nhập'),
        ('expense', 'Chi tiêu'),
    ]

    name = models.CharField(
        max_length=100,
        help_text="Category name"
    )
    icon = models.CharField(
        max_length=10,
        default='⚡',
        help_text="Emoji icon for the category"
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        help_text="Category type: income or expense"
    )
    color = models.CharField(
        max_length=7,
        default='#22c55e',
        help_text="Hex color code for UI"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when category was created"
    )

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['type', 'name']

    def __str__(self) -> str:
        """Return string representation of the category."""
        return f"{self.icon} {self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    """
    Transaction model for tracking income and expense transactions.

    Attributes:
        user: The user who owns this transaction
        category: The category this transaction belongs to
        type: Type of transaction - 'income' or 'expense'
        amount: The transaction amount (must be >= 0.01)
        date: The date when the transaction occurred
        note: Optional note/description for the transaction
        created_at: Timestamp when the transaction was created
        updated_at: Timestamp when the transaction was last updated
    """

    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Thu nhập'),
        ('expense', 'Chi tiêu'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Người dùng'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='Danh mục'
    )
    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='Loại giao dịch'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Số tiền'
    )
    date = models.DateField(verbose_name='Ngày giao dịch')
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name='Ghi chú'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Giao dịch'
        verbose_name_plural = 'Giao dịch'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'type']),
            models.Index(fields=['category']),
        ]

    def __str__(self) -> str:
        """Return string representation of the transaction."""
        return f"{self.get_type_display()} - {self.amount} VND - {self.date}"

    def save(self, *args, **kwargs):
        """
        Save the transaction with validation.

        Validates that the transaction type matches the category type
        before saving.

        Raises:
            ValueError: If transaction type doesn't match category type
        """
        if self.category_id is not None:
            if self.category.type != self.type:
                raise ValueError(
                    f"Category type ({self.category.type}) must match "
                    f"transaction type ({self.type})"
                )
        super().save(*args, **kwargs)
