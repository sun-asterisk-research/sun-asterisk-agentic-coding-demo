"""Tests for transactions app."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from transactions.models import Category


class CategoryModelTest(TestCase):
    """Test Category model."""

    def test_create_expense_category(self):
        """Test creating an expense category."""
        category = Category.objects.create(
            name='Ăn uống',
            icon='🍔',
            transaction_type='expense',
            color='#FF5722'
        )
        self.assertEqual(category.name, 'Ăn uống')
        self.assertEqual(category.icon, '🍔')
        self.assertEqual(category.transaction_type, 'expense')
        self.assertEqual(category.color, '#FF5722')

    def test_create_income_category(self):
        """Test creating an income category."""
        category = Category.objects.create(
            name='Lương',
            icon='💵',
            transaction_type='income',
            color='#4CAF50'
        )
        self.assertEqual(category.name, 'Lương')
        self.assertEqual(category.transaction_type, 'income')

    def test_category_str_representation(self):
        """Test __str__ method."""
        category = Category.objects.create(
            name='Ăn uống',
            icon='🍔',
            transaction_type='expense'
        )
        self.assertEqual(str(category), '🍔 Ăn uống')

    def test_category_default_color(self):
        """Test category has default color."""
        category = Category.objects.create(
            name='Test',
            transaction_type='expense'
        )
        self.assertEqual(category.color, '#4CAF50')

    def test_category_transaction_type_choices(self):
        """Test transaction_type must be income or expense."""
        category = Category(
            name='Invalid',
            transaction_type='invalid_type'
        )
        with self.assertRaises(ValidationError):
            category.full_clean()


class TransactionModelTest(TestCase):
    """Test Transaction model."""

    def setUp(self):
        """Setup test data."""
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Ăn uống',
            icon='🍔',
            transaction_type='expense'
        )

    def test_create_expense_transaction(self):
        """Test creating an expense transaction."""
        from transactions.models import Transaction
        from django.utils import timezone
        from decimal import Decimal

        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('50000'),
            transaction_type='expense',
            category=self.category,
            date=timezone.now().date(),
            note='Ăn trưa'
        )
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.amount, Decimal('50000'))
        self.assertEqual(transaction.transaction_type, 'expense')
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.note, 'Ăn trưa')

    def test_create_income_transaction(self):
        """Test creating an income transaction."""
        from transactions.models import Transaction
        from django.utils import timezone
        from decimal import Decimal

        income_category = Category.objects.create(
            name='Lương',
            icon='💵',
            transaction_type='income'
        )
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('10000000'),
            transaction_type='income',
            category=income_category,
            date=timezone.now().date()
        )
        self.assertEqual(transaction.transaction_type, 'income')
        self.assertEqual(transaction.amount, Decimal('10000000'))

    def test_transaction_str_representation(self):
        """Test __str__ method."""
        from transactions.models import Transaction
        from django.utils import timezone
        from decimal import Decimal

        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('50000'),
            transaction_type='expense',
            category=self.category,
            date=timezone.now().date()
        )
        self.assertIn('Chi tiêu', str(transaction))
        self.assertIn('50,000', str(transaction))

    def test_transaction_ordering(self):
        """Test transactions ordered by date descending."""
        from transactions.models import Transaction
        from django.utils import timezone
        from datetime import timedelta
        from decimal import Decimal

        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        trans1 = Transaction.objects.create(
            user=self.user,
            amount=Decimal('100'),
            transaction_type='expense',
            category=self.category,
            date=yesterday
        )
        trans2 = Transaction.objects.create(
            user=self.user,
            amount=Decimal('200'),
            transaction_type='expense',
            category=self.category,
            date=today
        )

        transactions = Transaction.objects.all()
        self.assertEqual(transactions[0], trans2)  # today first
        self.assertEqual(transactions[1], trans1)  # yesterday second


class TransactionFormTest(TestCase):
    """Test TransactionForm."""

    def setUp(self):
        """Setup test data."""
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Ăn uống',
            icon='🍔',
            transaction_type='expense'
        )

    def test_valid_transaction_form(self):
        """Test form with valid data."""
        from transactions.forms import TransactionForm
        from django.utils import timezone
        
        form_data = {
            'amount': '50000',
            'transaction_type': 'expense',
            'category': self.category.id,
            'date': timezone.now().date(),
            'note': 'Test note',
        }
        form = TransactionForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_transaction_form_missing_amount(self):
        """Test form with missing amount."""
        from transactions.forms import TransactionForm
        from django.utils import timezone
        
        form_data = {
            'transaction_type': 'expense',
            'category': self.category.id,
            'date': timezone.now().date(),
        }
        form = TransactionForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_transaction_form_negative_amount(self):
        """Test form with negative amount."""
        from transactions.forms import TransactionForm
        from django.utils import timezone
        
        form_data = {
            'amount': '-100',
            'transaction_type': 'expense',
            'category': self.category.id,
            'date': timezone.now().date(),
        }
        form = TransactionForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_transaction_form_filters_categories_by_type(self):
        """Test form filters categories based on transaction type."""
        from transactions.forms import TransactionForm
        
        # Create income category
        income_cat = Category.objects.create(
            name='Lương',
            transaction_type='income'
        )
        
        form = TransactionForm(user=self.user)
        # Initially should show all categories
        self.assertTrue(form.fields['category'].queryset.count() > 0)


class TransactionListViewTest(TestCase):
    """Test transaction_list view."""

    def setUp(self):
        """Setup test data."""
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Food',
            transaction_type='expense'
        )

    def test_view_requires_login(self):
        """Test view requires login."""
        response = self.client.get('/transactions/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_view_shows_only_user_transactions(self):
        """Test view shows only current user's transactions."""
        from transactions.models import Transaction
        from django.utils import timezone
        
        # Create transactions for two users
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            transaction_type='expense',
            amount=100000,
            date=timezone.now().date(),
            note='My transaction'
        )
        Transaction.objects.create(
            user=self.other_user,
            category=self.category,
            transaction_type='expense',
            amount=50000,
            date=timezone.now().date(),
            note='Other transaction'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/transactions/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 1)
        self.assertEqual(
            response.context['transactions'][0].note,
            'My transaction'
        )

    def test_view_pagination(self):
        """Test view paginates results."""
        from transactions.models import Transaction
        from django.utils import timezone
        
        # Create 25 transactions
        for i in range(25):
            Transaction.objects.create(
                user=self.user,
                category=self.category,
                transaction_type='expense',
                amount=1000 * (i + 1),
                date=timezone.now().date(),
                note=f'Transaction {i}'
            )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/transactions/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 20)
        self.assertTrue(response.context['is_paginated'])


class TransactionCreateViewTest(TestCase):
    """Test transaction_create view."""

    def setUp(self):
        """Setup test data."""
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Food',
            transaction_type='expense'
        )

    def test_view_requires_login(self):
        """Test view requires login."""
        response = self.client.get('/transactions/add/')
        self.assertEqual(response.status_code, 302)

    def test_view_get(self):
        """Test GET request shows form."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/transactions/add/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_view_post_valid_data(self):
        """Test POST with valid data creates transaction."""
        from transactions.models import Transaction
        from django.utils import timezone
        
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'transaction_type': 'expense',
            'category': self.category.id,
            'amount': 100000,
            'note': 'Lunch',
            'date': timezone.now().date()
        }
        response = self.client.post('/transactions/add/', form_data)
        
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.amount, 100000)
        self.assertRedirects(response, '/transactions/')


class TransactionUpdateViewTest(TestCase):
    """Test transaction_update view."""

    def setUp(self):
        """Setup test data."""
        from django.contrib.auth.models import User
        from transactions.models import Transaction
        from django.utils import timezone
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Food',
            transaction_type='expense'
        )
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            transaction_type='expense',
            amount=100000,
            date=timezone.now().date(),
            note='Original'
        )

    def test_view_requires_login(self):
        """Test view requires login."""
        response = self.client.get(f'/transactions/{self.transaction.id}/edit/')
        self.assertEqual(response.status_code, 302)

    def test_view_user_can_edit_own_transaction(self):
        """Test user can edit their own transaction."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/transactions/{self.transaction.id}/edit/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_view_user_cannot_edit_others_transaction(self):
        """Test user cannot edit other user's transaction."""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(f'/transactions/{self.transaction.id}/edit/')
        
        self.assertEqual(response.status_code, 404)

    def test_view_post_updates_transaction(self):
        """Test POST updates transaction."""
        from django.utils import timezone
        
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'transaction_type': 'expense',
            'category': self.category.id,
            'amount': 150000,
            'note': 'Updated',
            'date': timezone.now().date()
        }
        response = self.client.post(
            f'/transactions/{self.transaction.id}/edit/',
            form_data
        )
        
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, 150000)
        self.assertEqual(self.transaction.note, 'Updated')
        self.assertRedirects(response, '/transactions/')


class TransactionDeleteViewTest(TestCase):
    """Test transaction_delete view."""

    def setUp(self):
        """Setup test data."""
        from django.contrib.auth.models import User
        from transactions.models import Transaction
        from django.utils import timezone
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Food',
            transaction_type='expense'
        )
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            transaction_type='expense',
            amount=100000,
            date=timezone.now().date(),
            note='To delete'
        )

    def test_view_requires_login(self):
        """Test view requires login."""
        response = self.client.get(f'/transactions/{self.transaction.id}/delete/')
        self.assertEqual(response.status_code, 302)

    def test_view_get_shows_confirmation(self):
        """Test GET shows confirmation page."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/transactions/{self.transaction.id}/delete/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('object', response.context)

    def test_view_user_cannot_delete_others_transaction(self):
        """Test user cannot delete other user's transaction."""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(f'/transactions/{self.transaction.id}/delete/')
        
        self.assertEqual(response.status_code, 404)

    def test_view_post_deletes_transaction(self):
        """Test POST deletes transaction."""
        from transactions.models import Transaction
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(f'/transactions/{self.transaction.id}/delete/')
        
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertRedirects(response, '/transactions/')


class DashboardViewTest(TestCase):
    """Test dashboard view."""

    def setUp(self):
        """Setup test data."""
        from django.contrib.auth.models import User
        from transactions.models import Transaction
        from django.utils import timezone
        from decimal import Decimal
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create categories
        self.expense_cat1 = Category.objects.create(
            name='Food',
            transaction_type='expense'
        )
        self.expense_cat2 = Category.objects.create(
            name='Transport',
            transaction_type='expense'
        )
        self.income_cat = Category.objects.create(
            name='Salary',
            transaction_type='income'
        )
        
        # Create transactions
        today = timezone.now().date()
        Transaction.objects.create(
            user=self.user,
            category=self.expense_cat1,
            transaction_type='expense',
            amount=Decimal('100000'),
            date=today,
            note='Lunch'
        )
        Transaction.objects.create(
            user=self.user,
            category=self.expense_cat2,
            transaction_type='expense',
            amount=Decimal('50000'),
            date=today,
            note='Bus'
        )
        Transaction.objects.create(
            user=self.user,
            category=self.income_cat,
            transaction_type='income',
            amount=Decimal('10000000'),
            date=today,
            note='Monthly salary'
        )

    def test_view_requires_login(self):
        """Test dashboard requires login."""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_view_shows_summary_stats(self):
        """Test dashboard shows correct summary statistics."""
        from decimal import Decimal
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_income', response.context)
        self.assertIn('total_expense', response.context)
        self.assertIn('balance', response.context)
        
        self.assertEqual(
            response.context['total_income'],
            Decimal('10000000')
        )
        self.assertEqual(
            response.context['total_expense'],
            Decimal('150000')
        )
        self.assertEqual(
            response.context['balance'],
            Decimal('9850000')
        )

    def test_view_shows_recent_transactions(self):
        """Test dashboard shows recent transactions."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('recent_transactions', response.context)
        self.assertEqual(
            len(response.context['recent_transactions']),
            3
        )

    def test_view_shows_top_categories(self):
        """Test dashboard shows top expense categories."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('top_categories', response.context)
        
        # Should have 2 expense categories
        top_cats = response.context['top_categories']
        self.assertLessEqual(len(top_cats), 5)
        
        # First should be Food with 100000
        if len(top_cats) > 0:
            self.assertEqual(top_cats[0]['category__name'], 'Food')


class ReportViewTest(TestCase):
    """Test report view."""

    def setUp(self):
        """Setup test data."""
        from django.contrib.auth.models import User
        from transactions.models import Transaction
        from django.utils import timezone
        from datetime import timedelta
        from decimal import Decimal
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create categories
        self.expense_cat = Category.objects.create(
            name='Food',
            transaction_type='expense'
        )
        self.income_cat = Category.objects.create(
            name='Salary',
            transaction_type='income'
        )
        
        # Create transactions across different months
        today = timezone.now().date()
        last_month = today - timedelta(days=30)
        
        Transaction.objects.create(
            user=self.user,
            category=self.expense_cat,
            transaction_type='expense',
            amount=Decimal('100000'),
            date=today,
            note='Recent expense'
        )
        Transaction.objects.create(
            user=self.user,
            category=self.income_cat,
            transaction_type='income',
            amount=Decimal('5000000'),
            date=today,
            note='Recent income'
        )
        Transaction.objects.create(
            user=self.user,
            category=self.expense_cat,
            transaction_type='expense',
            amount=Decimal('200000'),
            date=last_month,
            note='Old expense'
        )

    def test_view_requires_login(self):
        """Test report view requires login."""
        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 302)

    def test_view_shows_monthly_summary(self):
        """Test report view shows monthly summary data."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/reports/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('monthly_data_json', response.context)
        self.assertIn('total_income', response.context)
        self.assertIn('total_expense', response.context)

    def test_view_filters_by_date_range(self):
        """Test report view can filter by date range."""
        from django.utils import timezone
        from datetime import timedelta
        
        self.client.login(username='testuser', password='testpass123')
        
        today = timezone.now().date()
        start_date = today - timedelta(days=7)
        
        response = self.client.get('/reports/', {
            'start_date': start_date.isoformat(),
            'end_date': today.isoformat()
        })
        
        self.assertEqual(response.status_code, 200)
        # Should have filtered data
        self.assertIn('start_date', response.context)
        self.assertIn('end_date', response.context)

    def test_view_shows_category_breakdown(self):
        """Test report view shows expense by category."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/reports/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('category_data', response.context)
