from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    User profile model with additional information.

    Extends Django's User model with a one-to-one relationship to store
    additional user information like display name, avatar, and monthly budget.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Người dùng'
    )
    display_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Tên hiển thị'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Ảnh đại diện'
    )
    monthly_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Ngân sách tháng',
        help_text='Giới hạn chi tiêu hàng tháng'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Ngày tạo'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Ngày cập nhật'
    )

    class Meta:
        verbose_name = 'Hồ sơ người dùng'
        verbose_name_plural = 'Hồ sơ người dùng'

    def __str__(self) -> str:
        """Return string representation of user profile."""
        return f"Profile of {self.user.username}"
