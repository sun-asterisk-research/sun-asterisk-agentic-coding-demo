"""
Unit tests for the transactions app views.

This module contains comprehensive tests for transaction views
following TDD methodology.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
from transactions.models import Category, Transaction


class TransactionListViewTest(TestCase):
    """Test suite for TransactionListView."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()

        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )

        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
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

        # Create test transactions for user1
        today = date.today()
        for i in range(25):  # Create 25 transactions for pagination test
            Transaction.objects.create(
                user=self.user1,
                category=self.expense_category,
                type='expense',
                amount=Decimal('100.00') + i,
                date=today - timedelta(days=i),
                note=f'Test transaction {i}'
            )

        # Create transactions for user2
        Transaction.objects.create(
            user=self.user2,
            category=self.expense_category,
            type='expense',
            amount=Decimal('200.00'),
            date=today,
            note='User2 transaction'
        )

    def test_view_requires_authentication(self):
        """Test unauthenticated users are redirected to login."""
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_view_url_exists_at_desired_location(self):
        """Test view is accessible at expected URL."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get('/transactions/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test view is accessible by URL name."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test view uses the correct template."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertTemplateUsed(
            response,
            'transactions/transaction_list.html'
        )

    def test_view_shows_only_users_transactions(self):
        """Test view displays only current user's transactions."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))

        # Check user1 has transactions
        self.assertEqual(response.status_code, 200)
        transactions = response.context['transaction_list']

        # All transactions should belong to user1
        for transaction in transactions:
            self.assertEqual(transaction.user, self.user1)

        # User2's transaction should not appear
        user2_transaction = Transaction.objects.filter(user=self.user2).first()
        self.assertNotIn(user2_transaction, transactions)

    def test_view_pagination_20_items_per_page(self):
        """Test view paginates with 20 items per page."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))

        # Check pagination is enabled
        self.assertTrue(response.context['is_paginated'])

        # Check first page has 20 items
        self.assertEqual(len(response.context['transaction_list']), 20)

    def test_view_pagination_second_page(self):
        """Test view pagination second page works correctly."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_list') + '?page=2'
        )

        # Check second page exists
        self.assertEqual(response.status_code, 200)

        # Second page should have remaining items (25 total - 20 on first page)
        self.assertEqual(len(response.context['transaction_list']), 5)

    def test_view_context_contains_categories(self):
        """Test view provides categories in context for filtering."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))

        self.assertIn('categories', response.context)
        categories = response.context['categories']

        self.assertIn(self.income_category, categories)
        self.assertIn(self.expense_category, categories)

    def test_view_filter_by_type_income(self):
        """Test view filters transactions by income type."""
        # Create income transaction
        Transaction.objects.create(
            user=self.user1,
            category=self.income_category,
            type='income',
            amount=Decimal('5000.00'),
            date=date.today(),
            note='Salary'
        )

        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_list') + '?type=income'
        )

        self.assertEqual(response.status_code, 200)
        transactions = response.context['transaction_list']

        # All transactions should be income type
        for transaction in transactions:
            self.assertEqual(transaction.type, 'income')

    def test_view_filter_by_type_expense(self):
        """Test view filters transactions by expense type."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_list') + '?type=expense'
        )

        self.assertEqual(response.status_code, 200)
        transactions = response.context['transaction_list']

        # All transactions should be expense type
        for transaction in transactions:
            self.assertEqual(transaction.type, 'expense')

    def test_view_filter_by_category(self):
        """Test view filters transactions by category."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_list') +
            f'?category={self.expense_category.id}'
        )

        self.assertEqual(response.status_code, 200)
        transactions = response.context['transaction_list']

        # All transactions should have the specified category
        for transaction in transactions:
            self.assertEqual(transaction.category, self.expense_category)

    def test_view_filter_by_date_from(self):
        """Test view filters transactions from a specific date."""
        self.client.login(username='testuser1', password='testpass123')

        date_from = date.today() - timedelta(days=5)
        response = self.client.get(
            reverse('transactions:transaction_list') +
            f'?date_from={date_from.isoformat()}'
        )

        self.assertEqual(response.status_code, 200)
        transactions = response.context['transaction_list']

        # All transactions should be from date_from onwards
        for transaction in transactions:
            self.assertGreaterEqual(transaction.date, date_from)

    def test_view_filter_by_date_to(self):
        """Test view filters transactions up to a specific date."""
        self.client.login(username='testuser1', password='testpass123')

        date_to = date.today() - timedelta(days=10)
        response = self.client.get(
            reverse('transactions:transaction_list') +
            f'?date_to={date_to.isoformat()}'
        )

        self.assertEqual(response.status_code, 200)
        transactions = response.context['transaction_list']

        # All transactions should be up to date_to
        for transaction in transactions:
            self.assertLessEqual(transaction.date, date_to)

    def test_view_filter_by_date_range(self):
        """Test view filters transactions by date range."""
        self.client.login(username='testuser1', password='testpass123')

        date_from = date.today() - timedelta(days=10)
        date_to = date.today() - timedelta(days=5)

        response = self.client.get(
            reverse('transactions:transaction_list') +
            f'?date_from={date_from.isoformat()}&date_to={date_to.isoformat()}'
        )

        self.assertEqual(response.status_code, 200)
        transactions = response.context['transaction_list']

        # All transactions should be within the date range
        for transaction in transactions:
            self.assertGreaterEqual(transaction.date, date_from)
            self.assertLessEqual(transaction.date, date_to)

    def test_view_filter_multiple_parameters(self):
        """Test view filters with multiple parameters simultaneously."""
        self.client.login(username='testuser1', password='testpass123')

        date_from = date.today() - timedelta(days=15)

        response = self.client.get(
            reverse('transactions:transaction_list') +
            f'?type=expense&category={self.expense_category.id}' +
            f'&date_from={date_from.isoformat()}'
        )

        self.assertEqual(response.status_code, 200)
        transactions = response.context['transaction_list']

        # All transactions should match all filters
        for transaction in transactions:
            self.assertEqual(transaction.type, 'expense')
            self.assertEqual(transaction.category, self.expense_category)
            self.assertGreaterEqual(transaction.date, date_from)

    def test_view_displays_transaction_count(self):
        """Test view context includes total transaction count."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))

        # Should have paginator with count
        self.assertIn('paginator', response.context)
        self.assertEqual(response.context['paginator'].count, 25)

    def test_view_empty_results_when_no_transactions(self):
        """Test view handles empty results gracefully."""
        # Create new user with no transactions
        user3 = User.objects.create_user(
            username='testuser3',
            password='testpass123'
        )

        self.client.login(username='testuser3', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transaction_list']), 0)
        self.assertFalse(response.context['is_paginated'])

    def test_view_ordering_by_date_descending(self):
        """Test view orders transactions by date (newest first)."""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))

        transactions = list(response.context['transaction_list'])

        # Check transactions are ordered by date descending
        for i in range(len(transactions) - 1):
            self.assertGreaterEqual(
                transactions[i].date,
                transactions[i + 1].date
            )
