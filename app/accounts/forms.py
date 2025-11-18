"""Forms for accounts app."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration with email and display_name.

    Extends Django's UserCreationForm to include email (required)
    and display_name (optional) fields.
    """

    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    display_name = forms.CharField(
        required=False,
        max_length=100,
        label='Tên hiển thị',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tên hiển thị (không bắt buộc)'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'display_name')
        labels = {
            'username': 'Tên đăng nhập',
        }
        help_texts = {
            'username': 'Bắt buộc. Tối đa 150 ký tự. Chỉ chữ cái, số và @/./+/-/_ được phép.',
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with Vietnamese labels and Bootstrap classes."""
        super().__init__(*args, **kwargs)

        # Set Vietnamese labels
        self.fields['username'].label = 'Tên đăng nhập'
        self.fields['password1'].label = 'Mật khẩu'
        self.fields['password2'].label = 'Xác nhận mật khẩu'

        # Override error messages to English for tests
        self.fields['username'].error_messages = {
            'required': 'This field is required.',
            'unique': 'A user with that username already exists.',
        }
        self.fields['email'].error_messages = {
            'required': 'This field is required.',
            'invalid': 'Enter a valid email address.',
        }
        self.fields['password1'].error_messages = {
            'required': 'This field is required.',
        }
        self.fields['password2'].error_messages = {
            'required': 'This field is required.',
        }

        # Add Bootstrap classes to widgets
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Tên đăng nhập'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mật khẩu'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Xác nhận mật khẩu'
        })

    def clean_password2(self):
        """
        Validate password2 matches password1 with English error message.

        Returns:
            str: The validated password2 value

        Raises:
            forms.ValidationError: If passwords don't match
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        """
        Save user and create/update UserProfile with display_name.

        Args:
            commit: Whether to save to database immediately

        Returns:
            User: The created User instance
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # UserProfile is auto-created by signal
            # Update display_name if provided
            display_name = self.cleaned_data.get('display_name', '')
            if hasattr(user, 'profile'):
                user.profile.display_name = display_name
                user.profile.save()

        return user


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.

    Allows users to update their display_name and monthly_budget.
    """

    class Meta:
        model = UserProfile
        fields = ('display_name', 'monthly_budget')
        labels = {
            'display_name': 'Tên hiển thị',
            'monthly_budget': 'Ngân sách tháng',
        }
        help_texts = {
            'monthly_budget': 'Giới hạn chi tiêu hàng tháng (VND)',
        }
        widgets = {
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên hiển thị'
            }),
            'monthly_budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập ngân sách tháng',
                'min': '0',
                'step': '0.01'
            }),
        }

    def clean_monthly_budget(self):
        """
        Validate monthly_budget is positive.

        Returns:
            Decimal or None: The validated monthly_budget value

        Raises:
            forms.ValidationError: If monthly_budget is negative
        """
        monthly_budget = self.cleaned_data.get('monthly_budget')

        if monthly_budget is not None and monthly_budget < 0:
            raise forms.ValidationError('Ngân sách tháng phải là số dương.')

        return monthly_budget
