"""Forms for transactions app."""
from django import forms
from django.core.exceptions import ValidationError
from .models import Transaction, Category


class TransactionForm(forms.ModelForm):
    """Form for creating/editing transactions."""
    
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'category', 'date', 'note']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập số tiền',
                'min': '0',
                'step': '0.01'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ghi chú (tùy chọn)'
            }),
        }
        labels = {
            'amount': 'Số tiền',
            'transaction_type': 'Loại giao dịch',
            'category': 'Danh mục',
            'date': 'Ngày',
            'note': 'Ghi chú',
        }
        help_texts = {
            'amount': 'Nhập số tiền (VNĐ). Ví dụ: 50000',
            'transaction_type': 'Chọn thu nhập hoặc chi tiêu',
            'category': 'Chọn danh mục phù hợp với giao dịch',
            'date': 'Ngày thực hiện giao dịch',
            'note': 'Thêm ghi chú về giao dịch (không bắt buộc)',
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with user context."""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set default date to today if creating new transaction
        if not self.instance.pk:
            from django.utils import timezone
            self.fields['date'].initial = timezone.now().date()

    def clean_amount(self):
        """Validate amount is positive."""
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise ValidationError('Số tiền phải lớn hơn 0')
        return amount

    def save(self, commit=True):
        """Save transaction with user."""
        transaction = super().save(commit=False)
        if self.user:
            transaction.user = self.user
        if commit:
            transaction.save()
        return transaction
