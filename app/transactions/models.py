"""Models for transactions app."""
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Danh mục thu chi."""

    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Thu nhập'),
        ('expense', 'Chi tiêu'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Tên danh mục"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icon (emoji)"
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name="Loại giao dịch"
    )
    color = models.CharField(
        max_length=7,
        default="#4CAF50",
        verbose_name="Màu sắc"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['transaction_type', 'name']

    def __str__(self):
        """String representation."""
        if self.icon:
            return f"{self.icon} {self.name}"
        return self.name


class Transaction(models.Model):
    """Giao dịch thu chi."""

    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Thu nhập'),
        ('expense', 'Chi tiêu'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="Người dùng"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Số tiền"
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name="Loại giao dịch"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name="Danh mục"
    )
    date = models.DateField(
        verbose_name="Ngày giao dịch"
    )
    note = models.TextField(
        blank=True,
        verbose_name="Ghi chú"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Giao dịch"
        verbose_name_plural = "Giao dịch"
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'transaction_type']),
        ]

    def __str__(self):
        """String representation."""
        type_display = self.get_transaction_type_display()
        return f"{type_display} - {self.amount:,} VNĐ - {self.date}"
