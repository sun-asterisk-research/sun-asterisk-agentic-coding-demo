"""
Unit tests for the transactions app templates.

This module contains tests for transaction_list.html and transaction_form.html
following TDD methodology.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta
from transactions.models import Category, Transaction


class TransactionListTemplateTest(TestCase):
    """Test suite for transaction_list.html template."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

        # Create categories
        self.expense_category = Category.objects.create(
            name='Food',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )
        self.income_category = Category.objects.create(
            name='Salary',
            type='income',
            icon='💰',
            color='#22c55e'
        )

        # Create test transactions
        self.transaction1 = Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today(),
            note='Test expense'
        )
        self.transaction2 = Transaction.objects.create(
            user=self.user,
            category=self.income_category,
            type='income',
            amount=Decimal('5000.00'),
            date=date.today() - timedelta(days=1),
            note='Test income'
        )

    def test_template_extends_base(self):
        """Test transaction_list.html extends base.html."""
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(
            response,
            'transactions/transaction_list.html'
        )

    def test_template_displays_page_title(self):
        """Test template displays correct page title."""
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertContains(response, 'Transactions')

    def test_template_displays_add_transaction_button(self):
        """Test template has 'Add Transaction' button."""
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertContains(response, 'Add Transaction')
        # Check for link to create view
        self.assertContains(
            response,
            reverse('transactions:transaction_create')
        )

    def test_template_displays_transactions_table(self):
        """Test template displays transactions in table format."""
        response = self.client.get(reverse('transactions:transaction_list'))
        # Check for table headers
        self.assertContains(response, 'Date')
        self.assertContains(response, 'Category')
        self.assertContains(response, 'Type')
        self.assertContains(response, 'Amount')
        self.assertContains(response, 'Note')
        self.assertContains(response, 'Actions')

    def test_template_displays_transaction_data(self):
        """Test template displays actual transaction data."""
        response = self.client.get(reverse('transactions:transaction_list'))
        # Check for transaction1 data
        self.assertContains(response, self.transaction1.category.name)
        # Check for amount (may have different formatting)
        self.assertContains(response, '100')
        self.assertContains(response, 'Test expense')

        # Check for transaction2 data
        self.assertContains(response, self.transaction2.category.name)
        self.assertContains(response, '5000')
        self.assertContains(response, 'Test income')

    def test_template_displays_edit_buttons(self):
        """Test template displays Edit buttons for each transaction."""
        response = self.client.get(reverse('transactions:transaction_list'))
        # Check for edit links
        edit_url1 = reverse(
            'transactions:transaction_update',
            kwargs={'pk': self.transaction1.pk}
        )
        edit_url2 = reverse(
            'transactions:transaction_update',
            kwargs={'pk': self.transaction2.pk}
        )
        self.assertContains(response, edit_url1)
        self.assertContains(response, edit_url2)

    def test_template_displays_delete_buttons(self):
        """Test template displays Delete buttons for each transaction."""
        response = self.client.get(reverse('transactions:transaction_list'))
        # Check for delete links
        delete_url1 = reverse(
            'transactions:transaction_delete',
            kwargs={'pk': self.transaction1.pk}
        )
        delete_url2 = reverse(
            'transactions:transaction_delete',
            kwargs={'pk': self.transaction2.pk}
        )
        self.assertContains(response, delete_url1)
        self.assertContains(response, delete_url2)

    def test_template_has_filter_form(self):
        """Test template includes filter form with all fields."""
        response = self.client.get(reverse('transactions:transaction_list'))
        # Check for filter inputs
        self.assertContains(response, 'date_from')
        self.assertContains(response, 'date_to')
        self.assertContains(response, 'category')
        self.assertContains(response, 'type')

    def test_template_has_type_filter_options(self):
        """Test template includes type filter with income/expense options."""
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertContains(response, 'income')
        self.assertContains(response, 'expense')

    def test_template_has_pagination_controls(self):
        """Test template includes pagination when needed."""
        # Create 25 transactions to trigger pagination (assuming 20/page)
        for i in range(23):  # Already have 2
            Transaction.objects.create(
                user=self.user,
                category=self.expense_category,
                type='expense',
                amount=Decimal('50.00'),
                date=date.today(),
                note=f'Transaction {i}'
            )

        response = self.client.get(reverse('transactions:transaction_list'))
        # Check for pagination elements
        self.assertContains(response, 'pagination')

    def test_template_displays_category_icons(self):
        """Test template displays category icons (emoji)."""
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertContains(response, self.expense_category.icon)
        self.assertContains(response, self.income_category.icon)

    def test_template_uses_bootstrap_styling(self):
        """Test template uses Bootstrap 5 classes."""
        response = self.client.get(reverse('transactions:transaction_list'))
        # Check for common Bootstrap classes
        self.assertContains(response, 'table')
        self.assertContains(response, 'btn')
        self.assertContains(response, 'card')

    def test_template_displays_empty_state(self):
        """Test template displays empty state when no transactions."""
        # Delete all transactions
        Transaction.objects.all().delete()

        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertContains(
            response,
            'No transactions found',
            status_code=200
        )

    def test_template_responsive_design_elements(self):
        """Test template includes responsive design classes."""
        response = self.client.get(reverse('transactions:transaction_list'))
        # Check for responsive classes
        self.assertContains(response, 'container')
        self.assertContains(response, 'table-responsive')


class TransactionFormTemplateTest(TestCase):
    """Test suite for transaction_form.html template."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

        # Create categories
        self.expense_category = Category.objects.create(
            name='Food',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )
        self.income_category = Category.objects.create(
            name='Salary',
            type='income',
            icon='💰',
            color='#22c55e'
        )

    def test_create_form_template_extends_base(self):
        """Test transaction_form.html extends base.html."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(
            response,
            'transactions/transaction_form.html'
        )

    def test_create_form_displays_title(self):
        """Test form template displays 'Add Transaction' title."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        self.assertContains(response, 'Add Transaction')

    def test_update_form_displays_title(self):
        """Test form template displays 'Edit Transaction' title."""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today(),
            note='Test'
        )

        response = self.client.get(
            reverse(
                'transactions:transaction_update',
                kwargs={'pk': transaction.pk}
            )
        )
        self.assertContains(response, 'Edit Transaction')

    def test_form_has_all_required_fields(self):
        """Test form template includes all required fields."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        # Check for form fields
        self.assertContains(response, 'name="type"')
        self.assertContains(response, 'name="category"')
        self.assertContains(response, 'name="amount"')
        self.assertContains(response, 'name="date"')
        self.assertContains(response, 'name="note"')

    def test_form_has_type_radio_buttons(self):
        """Test form includes type radio buttons for income/expense."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        # Check for type field options
        self.assertContains(response, 'income')
        self.assertContains(response, 'expense')
        self.assertContains(response, 'type="radio"')

    def test_form_has_category_dropdown(self):
        """Test form includes category dropdown."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        self.assertContains(response, '<select')
        self.assertContains(response, 'name="category"')

    def test_form_has_amount_input(self):
        """Test form includes amount input field."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        self.assertContains(response, 'name="amount"')
        self.assertContains(response, 'type="number"')

    def test_form_has_date_input(self):
        """Test form includes date input field."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        self.assertContains(response, 'name="date"')
        self.assertContains(response, 'type="date"')

    def test_form_has_note_textarea(self):
        """Test form includes note textarea field."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        self.assertContains(response, 'name="note"')
        self.assertContains(response, '<textarea')

    def test_form_has_submit_button(self):
        """Test form includes submit button."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, 'Save')

    def test_form_has_cancel_button(self):
        """Test form includes cancel button linking back to list."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        self.assertContains(response, 'Cancel')
        self.assertContains(
            response,
            reverse('transactions:transaction_list')
        )

    def test_form_includes_ajax_script(self):
        """Test form includes JavaScript for AJAX category filtering."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        # Check for script tag
        self.assertContains(response, '<script>')
        # Check for AJAX-related keywords
        self.assertContains(response, 'addEventListener')

    def test_form_uses_bootstrap_styling(self):
        """Test form uses Bootstrap 5 styling."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        # Check for Bootstrap form classes
        self.assertContains(response, 'form-control')
        self.assertContains(response, 'form-label')
        self.assertContains(response, 'btn')

    def test_form_displays_validation_errors(self):
        """Test form displays validation errors when submitted with invalid data."""
        response = self.client.post(
            reverse('transactions:transaction_create'),
            data={
                'type': 'expense',
                'amount': '-100',  # Invalid negative amount
                'date': date.today(),
            }
        )
        # Check for error messages
        self.assertContains(
            response,
            'error',
            status_code=200
        )

    def test_form_has_green_white_color_scheme(self):
        """Test form follows green and white color scheme."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        # Check for primary green color or btn-primary
        self.assertContains(response, 'btn-primary')

    def test_form_responsive_design(self):
        """Test form includes responsive design elements."""
        response = self.client.get(
            reverse('transactions:transaction_create')
        )
        # Check for responsive container
        self.assertContains(response, 'container')
        self.assertContains(response, 'card')

    def test_update_form_prepopulates_data(self):
        """Test update form prepopulates with existing transaction data."""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            type='expense',
            amount=Decimal('150.50'),
            date=date.today(),
            note='Existing transaction'
        )

        response = self.client.get(
            reverse(
                'transactions:transaction_update',
                kwargs={'pk': transaction.pk}
            )
        )
        # Check for prepopulated values (amount may be formatted differently)
        self.assertContains(response, '150')
        self.assertContains(response, 'Existing transaction')
        self.assertContains(response, 'expense')
