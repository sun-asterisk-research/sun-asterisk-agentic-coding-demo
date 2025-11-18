"""
Tests for ReportsView.

This module contains tests for the reports view functionality.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from decimal import Decimal
from transactions.models import Transaction, Category


class ReportsViewTest(TestCase):
    """Test suite for ReportsView."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )

        # Create test categories
        self.income_category = Category.objects.create(
            name='Salary',
            type='income',
            icon='💰',
            color='#22c55e'
        )
        self.expense_category = Category.objects.create(
            name='Food',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )

        # Create test transactions
        today = date.today()
        self.transaction1 = Transaction.objects.create(
            user=self.user,
            category=self.income_category,
            type='income',
            amount=Decimal('5000.00'),
            date=today,
            note='Test income'
        )
        self.transaction2 = Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            type='expense',
            amount=Decimal('500.00'),
            date=today,
            note='Test expense'
        )
        self.transaction3 = Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            type='expense',
            amount=Decimal('300.00'),
            date=today - timedelta(days=1),
            note='Yesterday expense'
        )

        # Create transaction for other user (should not appear)
        self.other_transaction = Transaction.objects.create(
            user=self.other_user,
            category=self.income_category,
            type='income',
            amount=Decimal('10000.00'),
            date=today,
            note='Other user income'
        )

    def test_view_url_exists_at_desired_location(self):
        """Test view is accessible at expected URL."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test view is accessible by URL name."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:reports'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test view uses the correct template."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:reports'))
        self.assertTemplateUsed(response, 'reports/reports.html')

    def test_view_redirects_when_not_authenticated(self):
        """Test view redirects unauthenticated users."""
        response = self.client.get(reverse('reports:reports'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_view_context_contains_time_ranges(self):
        """Test view provides time range filter options in context."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:reports'))

        self.assertIn('time_ranges', response.context)
        time_ranges = response.context['time_ranges']

        # Check that all required time ranges are present
        expected_ranges = ['today', 'this_week', 'this_month',
                           'this_year', 'custom']
        for range_key in expected_ranges:
            self.assertIn(range_key, [r[0] for r in time_ranges])

    def test_view_context_contains_current_range(self):
        """Test view provides current selected time range in context."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:reports'))

        self.assertIn('current_range', response.context)
        # Default should be 'this_month'
        self.assertEqual(response.context['current_range'], 'this_month')

    def test_view_filter_by_today(self):
        """Test filtering transactions by today."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') + '?range=today'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_range'], 'today')

        # Should show today's transactions only
        total_income = response.context['total_income']
        total_expense = response.context['total_expense']

        self.assertEqual(total_income, Decimal('5000.00'))
        self.assertEqual(total_expense, Decimal('500.00'))

    def test_view_filter_by_this_week(self):
        """Test filtering transactions by this week."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') + '?range=this_week'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_range'], 'this_week')

        # Should include all transactions from this week
        total_income = response.context['total_income']
        total_expense = response.context['total_expense']

        self.assertEqual(total_income, Decimal('5000.00'))
        self.assertEqual(total_expense, Decimal('800.00'))  # 500 + 300

    def test_view_filter_by_this_month(self):
        """Test filtering transactions by this month."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') + '?range=this_month'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_range'], 'this_month')

    def test_view_filter_by_this_year(self):
        """Test filtering transactions by this year."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') + '?range=this_year'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_range'], 'this_year')

    def test_view_filter_by_custom_date_range(self):
        """Test filtering transactions by custom date range."""
        self.client.login(username='testuser', password='testpass123')
        today = date.today()
        date_from = (today - timedelta(days=2)).strftime('%Y-%m-%d')
        date_to = today.strftime('%Y-%m-%d')

        response = self.client.get(
            reverse('reports:reports') +
            f'?range=custom&date_from={date_from}&date_to={date_to}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_range'], 'custom')

    def test_view_context_contains_statistics(self):
        """Test view provides income/expense statistics in context."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') + '?range=today'
        )

        # Check statistics keys in context
        self.assertIn('total_income', response.context)
        self.assertIn('total_expense', response.context)
        self.assertIn('balance', response.context)

        # Verify calculations
        total_income = response.context['total_income']
        total_expense = response.context['total_expense']
        balance = response.context['balance']

        self.assertEqual(total_income, Decimal('5000.00'))
        self.assertEqual(total_expense, Decimal('500.00'))
        self.assertEqual(balance, Decimal('4500.00'))

    def test_view_context_contains_category_breakdown(self):
        """Test view provides expense breakdown by category."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') + '?range=this_week'
        )

        self.assertIn('expense_by_category', response.context)
        expense_by_category = response.context['expense_by_category']

        # Should have breakdown by category
        self.assertTrue(len(expense_by_category) > 0)

        # Find Food category
        food_data = next(
            (item for item in expense_by_category
             if item['category__name'] == 'Food'),
            None
        )
        self.assertIsNotNone(food_data)
        self.assertEqual(food_data['total'], Decimal('800.00'))

    def test_view_context_contains_income_breakdown(self):
        """Test view provides income breakdown by category."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') + '?range=today'
        )

        self.assertIn('income_by_category', response.context)
        income_by_category = response.context['income_by_category']

        # Should have breakdown by category
        self.assertTrue(len(income_by_category) > 0)

        # Find Salary category
        salary_data = next(
            (item for item in income_by_category
             if item['category__name'] == 'Salary'),
            None
        )
        self.assertIsNotNone(salary_data)
        self.assertEqual(salary_data['total'], Decimal('5000.00'))

    def test_view_only_shows_user_transactions(self):
        """Test view only shows current user's transactions."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') + '?range=today'
        )

        total_income = response.context['total_income']

        # Should not include other_user's 10000 income
        self.assertEqual(total_income, Decimal('5000.00'))
        self.assertNotEqual(total_income, Decimal('15000.00'))

    def test_view_handles_invalid_date_range(self):
        """Test view handles invalid date range gracefully."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') + '?range=invalid_range'
        )

        self.assertEqual(response.status_code, 200)
        # Should default to this_month
        self.assertEqual(response.context['current_range'], 'this_month')

    def test_view_handles_invalid_custom_dates(self):
        """Test view handles invalid custom date format gracefully."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') +
            '?range=custom&date_from=invalid&date_to=invalid'
        )

        self.assertEqual(response.status_code, 200)
        # Should still work, just ignore invalid dates

    def test_view_context_contains_categories(self):
        """Test view provides categories for display."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:reports'))

        self.assertIn('categories', response.context)
        categories = response.context['categories']

        # Should contain both categories
        self.assertTrue(len(categories) >= 2)

    def test_view_balance_calculation(self):
        """Test balance is correctly calculated as income - expense."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('reports:reports') + '?range=this_week'
        )

        total_income = response.context['total_income']
        total_expense = response.context['total_expense']
        balance = response.context['balance']

        expected_balance = total_income - total_expense
        self.assertEqual(balance, expected_balance)
        self.assertEqual(balance, Decimal('4200.00'))  # 5000 - 800
