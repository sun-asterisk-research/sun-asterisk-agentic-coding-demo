"""
Unit tests for the transactions app forms.

This module contains comprehensive tests for TransactionForm
following TDD methodology.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from transactions.models import Category, Transaction
from transactions.forms import TransactionForm


class TransactionFormTest(TestCase):
    """Test suite for TransactionForm."""

    def setUp(self):
        """Set up test data that's needed for multiple tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create test categories
        self.income_category = Category.objects.create(
            name='Lương',
            icon='💰',
            type='income',
            color='#22c55e'
        )

        self.expense_category = Category.objects.create(
            name='Ăn uống',
            icon='🍔',
            type='expense',
            color='#ef4444'
        )

    def test_form_has_required_fields(self):
        """Test form includes all required fields."""
        form = TransactionForm()
        self.assertIn('type', form.fields)
        self.assertIn('category', form.fields)
        self.assertIn('amount', form.fields)
        self.assertIn('date', form.fields)
        self.assertIn('note', form.fields)

    def test_form_field_types(self):
        """Test form fields have correct types."""
        form = TransactionForm()
        from django import forms
        self.assertIsInstance(form.fields['type'], forms.ChoiceField)
        self.assertIsInstance(form.fields['category'], forms.ModelChoiceField)
        self.assertIsInstance(form.fields['amount'], forms.DecimalField)
        self.assertIsInstance(form.fields['date'], forms.DateField)
        self.assertIsInstance(form.fields['note'], forms.CharField)

    def test_form_valid_with_correct_data(self):
        """Test form is valid with correct data."""
        data = {
            'type': 'expense',
            'category': self.expense_category.id,
            'amount': '100.50',
            'date': date.today(),
            'note': 'Test transaction'
        }
        form = TransactionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_missing_type(self):
        """Test form is invalid when type field is missing."""
        data = {
            'category': self.expense_category.id,
            'amount': '100.50',
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('type', form.errors)

    def test_form_invalid_with_missing_category(self):
        """Test form is invalid when category field is missing."""
        data = {
            'type': 'expense',
            'amount': '100.50',
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_form_invalid_with_missing_amount(self):
        """Test form is invalid when amount field is missing."""
        data = {
            'type': 'expense',
            'category': self.expense_category.id,
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_form_invalid_with_missing_date(self):
        """Test form is invalid when date field is missing."""
        data = {
            'type': 'expense',
            'category': self.expense_category.id,
            'amount': '100.50',
        }
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_note_field_is_optional(self):
        """Test note field is optional and form is valid without it."""
        data = {
            'type': 'expense',
            'category': self.expense_category.id,
            'amount': '100.50',
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_negative_amount(self):
        """Test form is invalid with negative amount."""
        data = {
            'type': 'expense',
            'category': self.expense_category.id,
            'amount': '-50.00',
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_form_invalid_with_zero_amount(self):
        """Test form is invalid with zero amount."""
        data = {
            'type': 'expense',
            'category': self.expense_category.id,
            'amount': '0.00',
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_form_valid_with_minimum_amount(self):
        """Test form is valid with minimum amount (0.01)."""
        data = {
            'type': 'expense',
            'category': self.expense_category.id,
            'amount': '0.01',
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_type_doesnt_match_category(self):
        """Test form is invalid when transaction type doesn't match category type."""
        data = {
            'type': 'income',
            'category': self.expense_category.id,  # Expense category
            'amount': '100.00',
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_form_valid_when_type_matches_category_income(self):
        """Test form is valid when income type matches income category."""
        data = {
            'type': 'income',
            'category': self.income_category.id,
            'amount': '1000.00',
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_when_type_matches_category_expense(self):
        """Test form is valid when expense type matches expense category."""
        data = {
            'type': 'expense',
            'category': self.expense_category.id,
            'amount': '50.00',
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_category_queryset_filters_by_type(self):
        """Test form can filter categories by type."""
        # Create form with type parameter
        form = TransactionForm(transaction_type='income')

        # Get available categories
        category_ids = [cat.id for cat in form.fields['category'].queryset]

        # Should only include income categories
        self.assertIn(self.income_category.id, category_ids)
        self.assertNotIn(self.expense_category.id, category_ids)

    def test_form_saves_with_user(self):
        """Test form saves transaction with user."""
        data = {
            'type': 'expense',
            'category': self.expense_category.id,
            'amount': '100.00',
            'date': date.today(),
            'note': 'Test save'
        }
        form = TransactionForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

        transaction = form.save()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.amount, Decimal('100.00'))
        self.assertEqual(transaction.note, 'Test save')

    def test_form_type_choices(self):
        """Test form has correct type choices."""
        form = TransactionForm()
        choices = [choice[0] for choice in form.fields['type'].choices]
        # Remove empty choice if present
        choices = [c for c in choices if c]

        self.assertIn('income', choices)
        self.assertIn('expense', choices)

    def test_form_amount_decimal_places(self):
        """Test form accepts amounts with 2 decimal places."""
        data = {
            'type': 'expense',
            'category': self.expense_category.id,
            'amount': '123.45',
            'date': date.today(),
        }
        form = TransactionForm(data=data)
        self.assertTrue(form.is_valid())

        # Verify decimal places preserved
        self.assertEqual(form.cleaned_data['amount'], Decimal('123.45'))
