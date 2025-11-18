"""Forms for transactions app."""

from django import forms
from django.core.validators import MinValueValidator
from decimal import Decimal
from transactions.models import Transaction, Category


class TransactionForm(forms.ModelForm):
    """
    Form for creating and updating transactions.

    Provides dynamic category filtering based on transaction type
    and validates that category type matches transaction type.
    """

    type = forms.ChoiceField(
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        label='Loại giao dịch',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'transaction-type'
        })
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Danh mục',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'transaction-category'
        })
    )

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01'),
        label='Số tiền',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập số tiền',
            'step': '0.01',
            'min': '0.01'
        })
    )

    date = forms.DateField(
        label='Ngày giao dịch',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    note = forms.CharField(
        required=False,
        label='Ghi chú',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ghi chú (không bắt buộc)',
            'rows': 3
        })
    )

    class Meta:
        model = Transaction
        fields = ['type', 'category', 'amount', 'date', 'note']

    def __init__(self, *args, transaction_type=None, user=None, **kwargs):
        """
        Initialize form with optional transaction type filter.

        Args:
            transaction_type: Filter categories by this type ('income' or 'expense')
            user: The user creating/updating the transaction
        """
        super().__init__(*args, **kwargs)
        self.user = user

        # Filter categories by type if provided
        if transaction_type:
            self.fields['category'].queryset = Category.objects.filter(
                type=transaction_type
            )

        # Set initial type if provided
        if transaction_type and not self.instance.pk:
            self.initial['type'] = transaction_type

    def clean_category(self):
        """
        Validate category type matches transaction type.

        Returns:
            Category: The validated category

        Raises:
            forms.ValidationError: If category type doesn't match transaction type
        """
        category = self.cleaned_data.get('category')
        transaction_type = self.cleaned_data.get('type')

        if category and transaction_type:
            if category.type != transaction_type:
                raise forms.ValidationError(
                    f"Category type must match transaction type. "
                    f"Selected category is for {category.get_type_display()}, "
                    f"but transaction type is {dict(Transaction.TRANSACTION_TYPE_CHOICES).get(transaction_type)}."
                )

        return category

    def clean_amount(self):
        """
        Validate amount is at least 0.01.

        Returns:
            Decimal: The validated amount

        Raises:
            forms.ValidationError: If amount is less than 0.01
        """
        amount = self.cleaned_data.get('amount')

        if amount is not None and amount < Decimal('0.01'):
            raise forms.ValidationError(
                'Amount must be at least 0.01.'
            )

        return amount

    def save(self, commit=True):
        """
        Save transaction with user.

        Args:
            commit: Whether to save to database immediately

        Returns:
            Transaction: The created or updated Transaction instance
        """
        transaction = super().save(commit=False)

        # Set user if provided
        if self.user:
            transaction.user = self.user

        if commit:
            transaction.save()

        return transaction
