"""
Unit tests for the transactions app models.

This module contains comprehensive tests for the Category and Transaction models
following TDD methodology.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from decimal import Decimal
from datetime import date, timedelta
from transactions.models import Category, Transaction


class CategoryModelTest(TestCase):
    """Test suite for Category model."""

    def setUp(self):
        """Set up test data that's needed for multiple tests."""
        self.category = Category.objects.create(
            name='Ăn uống',
            icon='🍔',
            type='expense',
            color='#ef4444'
        )

    def test_category_creation(self):
        """Test Category instance can be created with valid data."""
        self.assertEqual(self.category.name, 'Ăn uống')
        self.assertEqual(self.category.icon, '🍔')
        self.assertEqual(self.category.type, 'expense')
        self.assertEqual(self.category.color, '#ef4444')
        self.assertIsNotNone(self.category.id)
        self.assertIsNotNone(self.category.created_at)

    def test_category_str_representation(self):
        """Test __str__ method returns expected string format."""
        expected = '🍔 Ăn uống (Chi tiêu)'
        self.assertEqual(str(self.category), expected)

    def test_category_name_max_length(self):
        """Test name field has max_length of 100 characters."""
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_category_icon_max_length(self):
        """Test icon field has max_length of 10 characters."""
        max_length = self.category._meta.get_field('icon').max_length
        self.assertEqual(max_length, 10)

    def test_category_icon_default_value(self):
        """Test icon field defaults to ⚡ when not provided."""
        category = Category.objects.create(
            name='Test Category',
            type='income'
        )
        self.assertEqual(category.icon, '⚡')

    def test_category_color_max_length(self):
        """Test color field has max_length of 7 characters."""
        max_length = self.category._meta.get_field('color').max_length
        self.assertEqual(max_length, 7)

    def test_category_color_default_value(self):
        """Test color field defaults to #22c55e when not provided."""
        category = Category.objects.create(
            name='Test Category',
            type='income'
        )
        self.assertEqual(category.color, '#22c55e')

    def test_category_type_choices(self):
        """Test type field has correct choices (income/expense)."""
        field = self.category._meta.get_field('type')
        choices = [choice[0] for choice in field.choices]
        self.assertIn('income', choices)
        self.assertIn('expense', choices)
        self.assertEqual(len(choices), 2)

    def test_category_type_income(self):
        """Test creating category with type income."""
        income_category = Category.objects.create(
            name='Lương',
            icon='💰',
            type='income',
            color='#22c55e'
        )
        self.assertEqual(income_category.type, 'income')
        self.assertEqual(income_category.get_type_display(), 'Thu nhập')

    def test_category_type_expense(self):
        """Test creating category with type expense."""
        self.assertEqual(self.category.type, 'expense')
        self.assertEqual(self.category.get_type_display(), 'Chi tiêu')

    def test_category_type_max_length(self):
        """Test type field has max_length of 10 characters."""
        max_length = self.category._meta.get_field('type').max_length
        self.assertEqual(max_length, 10)

    def test_category_name_required(self):
        """Test name field is required and cannot be blank."""
        category = Category(
            type='income',
            icon='💰'
        )
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_category_type_required(self):
        """Test type field is required and cannot be blank."""
        category = Category(
            name='Test Category',
            icon='💰'
        )
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_category_invalid_type(self):
        """Test invalid type value raises validation error."""
        category = Category(
            name='Test Category',
            type='invalid_type',
            icon='💰'
        )
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_category_created_at_auto_added(self):
        """Test created_at is automatically set on creation."""
        self.assertIsNotNone(self.category.created_at)

    def test_category_verbose_name(self):
        """Test model verbose_name is set correctly."""
        self.assertEqual(
            str(self.category._meta.verbose_name),
            'Danh mục'
        )

    def test_category_verbose_name_plural(self):
        """Test model verbose_name_plural is set correctly."""
        self.assertEqual(
            str(self.category._meta.verbose_name_plural),
            'Danh mục'
        )

    def test_category_ordering(self):
        """Test categories are ordered by type and name."""
        Category.objects.create(
            name='Xăng xe',
            icon='🚗',
            type='expense',
            color='#f97316'
        )
        Category.objects.create(
            name='Lương',
            icon='💰',
            type='income',
            color='#22c55e'
        )

        categories = Category.objects.all()
        # Check ordering: type first, then name
        ordering = self.category._meta.ordering
        self.assertEqual(ordering, ['type', 'name'])

    def test_category_with_long_name(self):
        """Test category can handle name up to max_length."""
        long_name = 'A' * 100
        category = Category.objects.create(
            name=long_name,
            type='income',
            icon='💰'
        )
        self.assertEqual(len(category.name), 100)
        self.assertEqual(category.name, long_name)

    def test_category_with_name_exceeding_max_length(self):
        """Test name exceeding max_length raises validation error."""
        long_name = 'A' * 101
        category = Category(
            name=long_name,
            type='income',
            icon='💰'
        )
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_category_color_hex_format(self):
        """Test color field accepts hex color format."""
        valid_colors = ['#000000', '#FFFFFF', '#22c55e', '#ef4444']
        for color in valid_colors:
            category = Category.objects.create(
                name=f'Test {color}',
                type='income',
                icon='💰',
                color=color
            )
            self.assertEqual(category.color, color)

    def test_category_icon_emoji(self):
        """Test icon field can store emoji characters."""
        emojis = ['🍔', '🚗', '🏠', '💰', '💼', '📈']
        for emoji in emojis:
            category = Category.objects.create(
                name=f'Test {emoji}',
                type='income',
                icon=emoji
            )
            self.assertEqual(category.icon, emoji)

    def test_multiple_categories_creation(self):
        """Test creating multiple categories."""
        initial_count = Category.objects.count()

        Category.objects.create(
            name='Xăng xe',
            icon='🚗',
            type='expense',
            color='#f97316'
        )
        Category.objects.create(
            name='Lương',
            icon='💰',
            type='income',
            color='#22c55e'
        )

        self.assertEqual(
            Category.objects.count(),
            initial_count + 2
        )

    def test_category_update(self):
        """Test updating category fields."""
        self.category.name = 'Ăn uống mới'
        self.category.icon = '🍕'
        self.category.color = '#ff0000'
        self.category.save()

        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.name, 'Ăn uống mới')
        self.assertEqual(updated_category.icon, '🍕')
        self.assertEqual(updated_category.color, '#ff0000')

    def test_category_delete(self):
        """Test deleting a category."""
        category_id = self.category.id
        self.category.delete()

        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category_id)

    def test_category_queryset_filter_by_type_income(self):
        """Test filtering categories by type income."""
        Category.objects.create(
            name='Lương',
            icon='💰',
            type='income',
            color='#22c55e'
        )
        Category.objects.create(
            name='Thưởng',
            icon='💼',
            type='income',
            color='#16a34a'
        )

        income_categories = Category.objects.filter(type='income')
        self.assertEqual(income_categories.count(), 2)
        for category in income_categories:
            self.assertEqual(category.type, 'income')

    def test_category_queryset_filter_by_type_expense(self):
        """Test filtering categories by type expense."""
        Category.objects.create(
            name='Xăng xe',
            icon='🚗',
            type='expense',
            color='#f97316'
        )

        expense_categories = Category.objects.filter(type='expense')
        self.assertEqual(expense_categories.count(), 2)  # Including setUp
        for category in expense_categories:
            self.assertEqual(category.type, 'expense')


class TransactionModelTest(TestCase):
    """
    Comprehensive test suite for Transaction model.

    Tests cover:
    - Model creation with valid data
    - Field validation (amount, type, date, note)
    - Required fields
    - __str__ representation
    - Relationships (user, category)
    - Custom save() method validation (type matches category type)
    - Ordering (by -date, -created_at)
    - Decimal precision
    - Indexes
    - Edge cases
    """

    def setUp(self):
        """Set up test data for multiple tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

    def test_transaction_creation_with_valid_data(self):
        """Test Transaction instance can be created with valid data."""
        category = Category.objects.create(
            name='Food & Beverage',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('100.50'),
            date=date.today(),
            note='Lunch at restaurant'
        )

        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.category, category)
        self.assertEqual(transaction.type, 'expense')
        self.assertEqual(transaction.amount, Decimal('100.50'))
        self.assertEqual(transaction.date, date.today())
        self.assertEqual(transaction.note, 'Lunch at restaurant')
        self.assertIsNotNone(transaction.id)
        self.assertIsNotNone(transaction.created_at)
        self.assertIsNotNone(transaction.updated_at)

    def test_transaction_str_representation(self):
        """Test __str__ method returns expected format."""
        category = Category.objects.create(
            name='Salary',
            type='income',
            icon='💰',
            color='#22c55e'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            type='income',
            amount=Decimal('5000000.00'),
            date=date(2025, 11, 1),
            note='Monthly salary'
        )

        expected = "Thu nhập - 5000000.00 VND - 2025-11-01"
        self.assertEqual(str(transaction), expected)

    def test_amount_minimum_validation(self):
        """Test amount field validates minimum value of 0.01."""
        category = Category.objects.create(
            name='Transportation',
            type='expense',
            icon='🚗',
            color='#f97316'
        )

        # Amount = 0 should fail
        transaction = Transaction(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('0.00'),
            date=date.today()
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()

        # Amount = 0.01 should pass
        transaction = Transaction(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('0.01'),
            date=date.today()
        )
        transaction.full_clean()  # Should not raise
        transaction.save()
        self.assertIsNotNone(transaction.id)

        # Negative amount should fail
        transaction = Transaction(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('-100.00'),
            date=date.today()
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()

    def test_amount_decimal_precision(self):
        """Test amount field handles decimal precision correctly."""
        category = Category.objects.create(
            name='Shopping',
            type='expense',
            icon='👕',
            color='#8b5cf6'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('1234567890.99'),
            date=date.today()
        )

        self.assertEqual(transaction.amount, Decimal('1234567890.99'))

    def test_user_relationship(self):
        """Test ForeignKey relationship with User."""
        category = Category.objects.create(
            name='Entertainment',
            type='expense',
            icon='🎬',
            color='#06b6d4'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('50.00'),
            date=date.today()
        )

        # Test forward relationship
        self.assertEqual(transaction.user, self.user)

        # Test reverse relationship (related_name='transactions')
        self.assertIn(transaction, self.user.transactions.all())
        self.assertEqual(self.user.transactions.count(), 1)

    def test_category_relationship(self):
        """Test ForeignKey relationship with Category."""
        category = Category.objects.create(
            name='Healthcare',
            type='expense',
            icon='💊',
            color='#ec4899'
        )

        transaction1 = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('200.00'),
            date=date.today()
        )

        transaction2 = Transaction.objects.create(
            user=self.user2,
            category=category,
            type='expense',
            amount=Decimal('150.00'),
            date=date.today()
        )

        # Test forward relationship
        self.assertEqual(transaction1.category, category)
        self.assertEqual(transaction2.category, category)

        # Test reverse relationship (related_name='transactions')
        self.assertIn(transaction1, category.transactions.all())
        self.assertIn(transaction2, category.transactions.all())
        self.assertEqual(category.transactions.count(), 2)

    def test_category_on_delete_protect(self):
        """Test Category cannot be deleted if it has transactions (PROTECT)."""
        category = Category.objects.create(
            name='Education',
            type='expense',
            icon='📚',
            color='#3b82f6'
        )

        Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('500.00'),
            date=date.today()
        )

        # Attempting to delete category should raise error
        with self.assertRaises(Exception):  # ProtectedError
            category.delete()

    def test_user_cascade_delete(self):
        """Test transactions are deleted when user is deleted (CASCADE)."""
        category = Category.objects.create(
            name='Gifts',
            type='expense',
            icon='🎁',
            color='#f59e0b'
        )

        Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )

        Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('200.00'),
            date=date.today()
        )

        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)

        # Delete user
        self.user.delete()

        # Transactions should be deleted
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 0)

    def test_type_choices_validation(self):
        """Test type field only accepts valid choices (income/expense)."""
        category = Category.objects.create(
            name='Other',
            type='expense',
            icon='⚡',
            color='#22c55e'
        )

        # Valid type 'expense'
        transaction = Transaction(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('50.00'),
            date=date.today()
        )
        transaction.full_clean()  # Should not raise
        transaction.save()

        # Valid type 'income'
        category_income = Category.objects.create(
            name='Salary',
            type='income',
            icon='💰',
            color='#22c55e'
        )
        transaction = Transaction(
            user=self.user,
            category=category_income,
            type='income',
            amount=Decimal('1000.00'),
            date=date.today()
        )
        transaction.full_clean()  # Should not raise
        transaction.save()

        # Invalid type should fail
        transaction = Transaction(
            user=self.user,
            category=category,
            type='invalid_type',
            amount=Decimal('50.00'),
            date=date.today()
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()

    def test_custom_save_validates_type_matches_category_type(self):
        """Test custom save() validates transaction type matches category type."""
        expense_category = Category.objects.create(
            name='Food',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )

        income_category = Category.objects.create(
            name='Salary',
            type='income',
            icon='💰',
            color='#22c55e'
        )

        # Matching types should work
        transaction = Transaction(
            user=self.user,
            category=expense_category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )
        transaction.save()  # Should not raise
        self.assertIsNotNone(transaction.id)

        # Mismatched types should fail
        transaction = Transaction(
            user=self.user,
            category=expense_category,
            type='income',  # Mismatch: category is expense, transaction is income
            amount=Decimal('100.00'),
            date=date.today()
        )
        with self.assertRaises(ValueError) as context:
            transaction.save()

        self.assertIn('must match', str(context.exception))

        # Reverse mismatch should also fail
        transaction = Transaction(
            user=self.user,
            category=income_category,
            type='expense',  # Mismatch: category is income, transaction is expense
            amount=Decimal('100.00'),
            date=date.today()
        )
        with self.assertRaises(ValueError):
            transaction.save()

    def test_required_fields(self):
        """Test required fields cannot be null or blank."""
        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='⚡',
            color='#22c55e'
        )

        # Missing user
        trans = Transaction(
            category=category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                trans.save()

        # Missing category
        trans = Transaction(
            user=self.user,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                trans.save()

        # Missing type
        trans = Transaction(
            user=self.user,
            category=category,
            amount=Decimal('100.00'),
            date=date.today()
        )
        with self.assertRaises(ValidationError):
            trans.full_clean()

        # Missing amount
        trans = Transaction(
            user=self.user,
            category=category,
            type='expense',
            date=date.today()
        )
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                trans.save()

        # Missing date
        trans = Transaction(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('100.00')
        )
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                trans.save()

    def test_note_field_optional(self):
        """Test note field is optional (blank=True, null=True)."""
        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='⚡',
            color='#22c55e'
        )

        # Transaction without note should work
        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )
        self.assertIsNone(transaction.note)

        # Transaction with note should work
        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('200.00'),
            date=date.today(),
            note='Test note'
        )
        self.assertEqual(transaction.note, 'Test note')

        # Transaction with empty string note should work
        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('300.00'),
            date=date.today(),
            note=''
        )
        self.assertEqual(transaction.note, '')

    def test_ordering_by_date_and_created_at(self):
        """Test default ordering is by -date, -created_at (newest first)."""
        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='⚡',
            color='#22c55e'
        )

        # Create transactions with different dates
        transaction1 = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today() - timedelta(days=2),
            note='Transaction 1 (oldest)'
        )

        transaction2 = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('200.00'),
            date=date.today(),
            note='Transaction 2 (newest by date)'
        )

        transaction3 = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('300.00'),
            date=date.today() - timedelta(days=1),
            note='Transaction 3 (middle)'
        )

        # Get all transactions
        transactions = Transaction.objects.all()

        # Should be ordered by -date (newest first)
        self.assertEqual(transactions[0], transaction2)  # Today
        self.assertEqual(transactions[1], transaction3)  # Yesterday
        self.assertEqual(transactions[2], transaction1)  # 2 days ago

    def test_ordering_by_created_at_when_same_date(self):
        """Test ordering by -created_at when dates are the same."""
        import time

        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='⚡',
            color='#22c55e'
        )

        # Create multiple transactions on the same date
        transaction1 = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today(),
            note='First'
        )

        time.sleep(0.01)  # Small delay to ensure different created_at

        transaction2 = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('200.00'),
            date=date.today(),
            note='Second'
        )

        time.sleep(0.01)

        transaction3 = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('300.00'),
            date=date.today(),
            note='Third'
        )

        # Get transactions for today
        transactions = Transaction.objects.filter(date=date.today())

        # Should be ordered by -created_at (most recent first) when dates are same
        self.assertEqual(transactions[0], transaction3)  # Created last
        self.assertEqual(transactions[1], transaction2)  # Created second
        self.assertEqual(transactions[2], transaction1)  # Created first

    def test_meta_verbose_names(self):
        """Test model Meta verbose names are set correctly."""
        self.assertEqual(Transaction._meta.verbose_name, 'Giao dịch')
        self.assertEqual(Transaction._meta.verbose_name_plural, 'Giao dịch')

    def test_indexes_exist(self):
        """Test database indexes are defined correctly."""
        # Get index definitions from Meta
        indexes = Transaction._meta.indexes

        # Should have 3 indexes
        self.assertEqual(len(indexes), 3)

        # Check index fields
        index_fields = [tuple(index.fields) for index in indexes]
        self.assertIn(('user', 'date'), index_fields)
        self.assertIn(('user', 'type'), index_fields)
        self.assertIn(('category',), index_fields)

    def test_income_transaction_complete_workflow(self):
        """Test creating and managing income transaction."""
        income_category = Category.objects.create(
            name='Salary',
            type='income',
            icon='💰',
            color='#22c55e'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=income_category,
            type='income',
            amount=Decimal('5000000.00'),
            date=date(2025, 11, 1),
            note='Monthly salary for November'
        )

        # Verify all fields
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.category, income_category)
        self.assertEqual(transaction.type, 'income')
        self.assertEqual(transaction.amount, Decimal('5000000.00'))
        self.assertEqual(transaction.date, date(2025, 11, 1))
        self.assertEqual(transaction.note, 'Monthly salary for November')

        # Verify it appears in queries
        self.assertIn(transaction, Transaction.objects.filter(type='income'))
        self.assertIn(transaction, self.user.transactions.all())

    def test_expense_transaction_complete_workflow(self):
        """Test creating and managing expense transaction."""
        expense_category = Category.objects.create(
            name='Food & Beverage',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=expense_category,
            type='expense',
            amount=Decimal('250.50'),
            date=date.today(),
            note='Lunch with friends'
        )

        # Verify all fields
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.category, expense_category)
        self.assertEqual(transaction.type, 'expense')
        self.assertEqual(transaction.amount, Decimal('250.50'))
        self.assertEqual(transaction.date, date.today())
        self.assertEqual(transaction.note, 'Lunch with friends')

        # Verify it appears in queries
        self.assertIn(transaction, Transaction.objects.filter(type='expense'))
        self.assertIn(transaction, self.user.transactions.all())

    def test_updated_at_changes_on_update(self):
        """Test updated_at timestamp changes when transaction is updated."""
        import time

        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='⚡',
            color='#22c55e'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )

        original_updated_at = transaction.updated_at

        time.sleep(0.01)  # Small delay

        # Update transaction
        transaction.amount = Decimal('200.00')
        transaction.save()

        # Refresh from database
        transaction.refresh_from_db()

        # updated_at should have changed
        self.assertGreater(transaction.updated_at, original_updated_at)

    def test_filter_by_user_and_date_index(self):
        """Test querying with user and date uses the index efficiently."""
        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='⚡',
            color='#22c55e'
        )

        # Create transactions for user1
        Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )

        Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('200.00'),
            date=date.today() - timedelta(days=1)
        )

        # Create transaction for user2
        Transaction.objects.create(
            user=self.user2,
            category=category,
            type='expense',
            amount=Decimal('300.00'),
            date=date.today()
        )

        # Filter by user and date
        transactions = Transaction.objects.filter(
            user=self.user,
            date=date.today()
        )

        self.assertEqual(transactions.count(), 1)
        self.assertEqual(transactions[0].amount, Decimal('100.00'))

    def test_filter_by_user_and_type_index(self):
        """Test querying with user and type uses the index efficiently."""
        expense_category = Category.objects.create(
            name='Food',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )

        income_category = Category.objects.create(
            name='Salary',
            type='income',
            icon='💰',
            color='#22c55e'
        )

        # Create mixed transactions
        Transaction.objects.create(
            user=self.user,
            category=expense_category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )

        Transaction.objects.create(
            user=self.user,
            category=income_category,
            type='income',
            amount=Decimal('5000.00'),
            date=date.today()
        )

        Transaction.objects.create(
            user=self.user2,
            category=expense_category,
            type='expense',
            amount=Decimal('200.00'),
            date=date.today()
        )

        # Filter by user and type
        transactions = Transaction.objects.filter(
            user=self.user,
            type='income'
        )

        self.assertEqual(transactions.count(), 1)
        self.assertEqual(transactions[0].amount, Decimal('5000.00'))

    def test_transaction_type_max_length(self):
        """Test type field has max_length of 10 characters."""
        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='⚡',
            color='#22c55e'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )

        max_length = transaction._meta.get_field('type').max_length
        self.assertEqual(max_length, 10)

    def test_amount_max_digits_and_decimal_places(self):
        """Test amount field has correct max_digits and decimal_places."""
        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='⚡',
            color='#22c55e'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )

        field = transaction._meta.get_field('amount')
        self.assertEqual(field.max_digits, 12)
        self.assertEqual(field.decimal_places, 2)

    def test_get_type_display(self):
        """Test get_type_display returns Vietnamese labels."""
        expense_category = Category.objects.create(
            name='Food',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )

        income_category = Category.objects.create(
            name='Salary',
            type='income',
            icon='💰',
            color='#22c55e'
        )

        expense_transaction = Transaction.objects.create(
            user=self.user,
            category=expense_category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today()
        )

        income_transaction = Transaction.objects.create(
            user=self.user,
            category=income_category,
            type='income',
            amount=Decimal('5000.00'),
            date=date.today()
        )

        self.assertEqual(expense_transaction.get_type_display(), 'Chi tiêu')
        self.assertEqual(income_transaction.get_type_display(), 'Thu nhập')


class CategoryAdminTest(TestCase):
    """Test suite for Category admin registration."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.category = Category.objects.create(
            name='Ăn uống',
            icon='🍔',
            type='expense',
            color='#ef4444'
        )

    def test_category_admin_is_registered(self):
        """Test Category model is registered with admin site."""
        from django.contrib import admin
        from transactions.models import Category

        self.assertIn(Category, admin.site._registry)

    def test_category_admin_list_display(self):
        """Test CategoryAdmin has correct list_display fields."""
        from django.contrib import admin
        from transactions.models import Category

        category_admin = admin.site._registry[Category]
        expected_list_display = ('icon', 'name', 'type', 'color')

        self.assertEqual(category_admin.list_display, expected_list_display)

    def test_category_admin_list_filter(self):
        """Test CategoryAdmin has type in list_filter."""
        from django.contrib import admin
        from transactions.models import Category

        category_admin = admin.site._registry[Category]
        expected_list_filter = ('type',)

        self.assertEqual(category_admin.list_filter, expected_list_filter)

    def test_category_admin_search_fields(self):
        """Test CategoryAdmin has name in search_fields."""
        from django.contrib import admin
        from transactions.models import Category

        category_admin = admin.site._registry[Category]
        expected_search_fields = ('name',)

        self.assertEqual(category_admin.search_fields, expected_search_fields)

    def test_category_admin_ordering(self):
        """Test CategoryAdmin has correct ordering."""
        from django.contrib import admin
        from transactions.models import Category

        category_admin = admin.site._registry[Category]
        expected_ordering = ('type', 'name')

        self.assertEqual(category_admin.ordering, expected_ordering)


class TransactionAdminTest(TestCase):
    """Test suite for Transaction admin registration."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Ăn uống',
            icon='🍔',
            type='expense',
            color='#ef4444'
        )
        self.transaction = Transaction.objects.create(
            user=self.regular_user,
            category=self.category,
            type='expense',
            amount=Decimal('100.50'),
            date=date.today(),
            note='Lunch'
        )

    def test_transaction_admin_is_registered(self):
        """Test Transaction model is registered with admin site."""
        from django.contrib import admin
        from transactions.models import Transaction

        self.assertIn(Transaction, admin.site._registry)

    def test_transaction_admin_list_display(self):
        """Test TransactionAdmin has correct list_display fields."""
        from django.contrib import admin
        from transactions.models import Transaction

        transaction_admin = admin.site._registry[Transaction]
        expected_list_display = (
            'date', 'user', 'category', 'type', 'formatted_amount', 'note_preview'
        )

        self.assertEqual(
            transaction_admin.list_display,
            expected_list_display
        )

    def test_transaction_admin_list_filter(self):
        """Test TransactionAdmin has correct list_filter fields."""
        from django.contrib import admin
        from transactions.models import Transaction

        transaction_admin = admin.site._registry[Transaction]
        expected_list_filter = ('type', 'category', 'date', 'user')

        self.assertEqual(
            transaction_admin.list_filter,
            expected_list_filter
        )

    def test_transaction_admin_search_fields(self):
        """Test TransactionAdmin has correct search_fields."""
        from django.contrib import admin
        from transactions.models import Transaction

        transaction_admin = admin.site._registry[Transaction]
        expected_search_fields = (
            'user__username', 'user__email', 'note', 'category__name'
        )

        self.assertEqual(
            transaction_admin.search_fields,
            expected_search_fields
        )

    def test_transaction_admin_date_hierarchy(self):
        """Test TransactionAdmin has date_hierarchy on date field."""
        from django.contrib import admin
        from transactions.models import Transaction

        transaction_admin = admin.site._registry[Transaction]

        self.assertEqual(transaction_admin.date_hierarchy, 'date')

    def test_transaction_admin_ordering(self):
        """Test TransactionAdmin has correct ordering."""
        from django.contrib import admin
        from transactions.models import Transaction

        transaction_admin = admin.site._registry[Transaction]
        expected_ordering = ('-date', '-created_at')

        self.assertEqual(transaction_admin.ordering, expected_ordering)


class SeedCategoriesCommandTest(TestCase):
    """Test suite for seed_categories management command."""

    def test_command_creates_17_categories(self):
        """Test command creates exactly 17 categories."""
        from django.core.management import call_command
        from io import StringIO

        # Ensure no categories exist initially
        Category.objects.all().delete()

        # Run the command
        out = StringIO()
        call_command('seed_categories', stdout=out)

        # Verify 17 categories were created
        self.assertEqual(Category.objects.count(), 17)

    def test_command_creates_11_expense_categories(self):
        """Test command creates 11 expense categories."""
        from django.core.management import call_command

        # Ensure no categories exist initially
        Category.objects.all().delete()

        # Run the command
        call_command('seed_categories')

        # Verify 11 expense categories
        expense_count = Category.objects.filter(type='expense').count()
        self.assertEqual(expense_count, 11)

    def test_command_creates_6_income_categories(self):
        """Test command creates 6 income categories."""
        from django.core.management import call_command

        # Ensure no categories exist initially
        Category.objects.all().delete()

        # Run the command
        call_command('seed_categories')

        # Verify 6 income categories
        income_count = Category.objects.filter(type='income').count()
        self.assertEqual(income_count, 6)

    def test_command_is_idempotent(self):
        """Test command doesn't create duplicates when run multiple times."""
        from django.core.management import call_command

        # Ensure no categories exist initially
        Category.objects.all().delete()

        # Run command twice
        call_command('seed_categories')
        call_command('seed_categories')

        # Should still only have 17 categories
        self.assertEqual(Category.objects.count(), 17)

    def test_command_creates_correct_expense_categories(self):
        """Test command creates all expected expense categories."""
        from django.core.management import call_command

        # Ensure no categories exist initially
        Category.objects.all().delete()

        # Run the command
        call_command('seed_categories')

        # Expected expense categories
        expected_expenses = [
            ('Ăn uống', '🍔', '#ef4444'),
            ('Xăng xe', '🚗', '#f97316'),
            ('Nhà cửa', '🏠', '#8b5cf6'),
            ('Mua sắm', '👕', '#ec4899'),
            ('Y tế', '💊', '#14b8a6'),
            ('Giáo dục', '📚', '#3b82f6'),
            ('Giải trí', '🎬', '#f59e0b'),
            ('Điện thoại/Internet', '📱', '#06b6d4'),
            ('Gia đình', '👨\u200d👩\u200d👧', '#84cc16'),
            ('Quà tặng', '🎁', '#a855f7'),
            ('Khác', '⚡', '#6b7280'),
        ]

        for name, icon, color in expected_expenses:
            category = Category.objects.filter(
                name=name,
                type='expense'
            ).first()
            self.assertIsNotNone(
                category,
                f"Category '{name}' not found"
            )
            self.assertEqual(category.icon, icon)
            self.assertEqual(category.color, color)

    def test_command_creates_correct_income_categories(self):
        """Test command creates all expected income categories."""
        from django.core.management import call_command

        # Ensure no categories exist initially
        Category.objects.all().delete()

        # Run the command
        call_command('seed_categories')

        # Expected income categories
        expected_incomes = [
            ('Lương', '💰', '#22c55e'),
            ('Thưởng', '💼', '#16a34a'),
            ('Đầu tư', '📈', '#15803d'),
            ('Thu nhập phụ', '🎯', '#059669'),
            ('Quà tặng', '🎁', '#10b981'),
            ('Khác', '⚡', '#14532d'),
        ]

        for name, icon, color in expected_incomes:
            category = Category.objects.filter(
                name=name,
                type='income'
            ).first()
            self.assertIsNotNone(
                category,
                f"Category '{name}' not found"
            )
            self.assertEqual(category.icon, icon)
            self.assertEqual(category.color, color)

    def test_command_outputs_success_message(self):
        """Test command outputs success message."""
        from django.core.management import call_command
        from io import StringIO

        # Ensure no categories exist initially
        Category.objects.all().delete()

        out = StringIO()
        call_command('seed_categories', stdout=out)

        output = out.getvalue()
        self.assertIn('Successfully seeded', output)
        self.assertIn('17 categories', output)
