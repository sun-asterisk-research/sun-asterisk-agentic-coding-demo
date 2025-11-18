"""
Tests for DashboardView.

This module contains comprehensive test cases for the DashboardView
including authentication, statistics calculation, and data filtering.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from decimal import Decimal
from django.utils import timezone
from transactions.models import Transaction, Category


class DashboardViewTest(TestCase):
    """Test suite for DashboardView."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create another user for isolation testing
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )

        # Create categories
        self.income_category = Category.objects.create(
            name='Lương',
            type='income',
            icon='💰',
            color='#22c55e'
        )

        self.expense_category = Category.objects.create(
            name='Ăn uống',
            type='expense',
            icon='🍜',
            color='#ef4444'
        )

        # Get current month's date range
        self.today = timezone.now().date()
        self.current_month_start = self.today.replace(day=1)

        # Create transactions for current month
        self.income1 = Transaction.objects.create(
            user=self.user,
            category=self.income_category,
            type='income',
            amount=Decimal('5000000.00'),
            date=self.today,
            note='Salary for current month'
        )

        self.income2 = Transaction.objects.create(
            user=self.user,
            category=self.income_category,
            type='income',
            amount=Decimal('2000000.00'),
            date=self.today - timedelta(days=5),
            note='Bonus'
        )

        self.expense1 = Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            type='expense',
            amount=Decimal('1500000.00'),
            date=self.today,
            note='Food expense'
        )

        self.expense2 = Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            type='expense',
            amount=Decimal('500000.00'),
            date=self.today - timedelta(days=3),
            note='Coffee'
        )

        # Create transaction for previous month (should not be included)
        if self.current_month_start.month > 1:
            prev_month_date = self.current_month_start - timedelta(days=1)
        else:
            prev_month_date = self.current_month_start.replace(
                year=self.current_month_start.year - 1,
                month=12
            )

        self.old_transaction = Transaction.objects.create(
            user=self.user,
            category=self.income_category,
            type='income',
            amount=Decimal('3000000.00'),
            date=prev_month_date,
            note='Previous month income'
        )

        # Create transaction for other user (should not be included)
        self.other_user_transaction = Transaction.objects.create(
            user=self.other_user,
            category=self.income_category,
            type='income',
            amount=Decimal('10000000.00'),
            date=self.today,
            note='Other user transaction'
        )

    def test_view_url_exists_at_desired_location(self):
        """Test dashboard view is accessible at expected URL."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/reports/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test dashboard view is accessible by URL name."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test dashboard view uses the correct template."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))
        self.assertTemplateUsed(response, 'reports/dashboard.html')

    def test_view_redirects_when_not_authenticated(self):
        """Test view redirects unauthenticated users to login page."""
        response = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_view_context_contains_total_income(self):
        """Test view provides total_income in context for current month."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        self.assertIn('total_income', response.context)
        expected_income = Decimal('7000000.00')
        self.assertEqual(response.context['total_income'], expected_income)

    def test_view_context_contains_total_expense(self):
        """Test view provides total_expense in context for current month."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        self.assertIn('total_expense', response.context)
        expected_expense = Decimal('2000000.00')
        self.assertEqual(response.context['total_expense'], expected_expense)

    def test_view_context_contains_balance(self):
        """Test view provides balance (income - expense) in context."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        self.assertIn('balance', response.context)
        expected_balance = Decimal('5000000.00')
        self.assertEqual(response.context['balance'], expected_balance)

    def test_view_context_contains_recent_transactions(self):
        """Test view provides recent transactions in context."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        self.assertIn('recent_transactions', response.context)
        recent_transactions = response.context['recent_transactions']
        self.assertIsNotNone(recent_transactions)
        self.assertLessEqual(len(recent_transactions), 10)

    def test_recent_transactions_ordered_by_date_descending(self):
        """Test recent transactions are ordered by date (newest first)."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        recent_transactions = list(response.context['recent_transactions'])

        if len(recent_transactions) > 1:
            for i in range(len(recent_transactions) - 1):
                self.assertGreaterEqual(
                    recent_transactions[i].date,
                    recent_transactions[i + 1].date
                )

    def test_recent_transactions_only_for_current_user(self):
        """Test recent transactions only include current user's data."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        recent_transactions = list(response.context['recent_transactions'])

        for transaction in recent_transactions:
            self.assertEqual(transaction.user, self.user)
            self.assertNotEqual(
                transaction.id,
                self.other_user_transaction.id
            )

    def test_statistics_only_for_current_month(self):
        """Test statistics only include current month's transactions."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        total_income = response.context['total_income']
        self.assertNotEqual(total_income, Decimal('10000000.00'))
        self.assertEqual(total_income, Decimal('7000000.00'))

    def test_statistics_only_for_current_user(self):
        """Test statistics only include current user's transactions."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        total_income = response.context['total_income']
        self.assertNotEqual(total_income, Decimal('17000000.00'))
        self.assertEqual(total_income, Decimal('7000000.00'))

    def test_zero_balance_when_no_transactions(self):
        """Test balance is zero when user has no transactions."""
        new_user = User.objects.create_user(
            username='newuser',
            password='testpass123'
        )

        self.client.login(username='newuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        self.assertEqual(response.context['total_income'], Decimal('0'))
        self.assertEqual(response.context['total_expense'], Decimal('0'))
        self.assertEqual(response.context['balance'], Decimal('0'))
        self.assertEqual(len(response.context['recent_transactions']), 0)

    def test_view_context_contains_current_month_info(self):
        """Test view provides current month information in context."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        self.assertIn('current_month', response.context)
        self.assertIn('current_year', response.context)
