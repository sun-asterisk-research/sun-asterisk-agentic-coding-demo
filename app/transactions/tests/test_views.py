"""
Unit tests for the transactions app views.

This module contains comprehensive tests for transaction views following TDD methodology.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from transactions.models import Category, Transaction


class TransactionCreateViewTest(TestCase):
    """Test suite for TransactionCreateView."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Food & Beverage',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )

    def test_view_url_exists_at_desired_location(self):
        """Test view is accessible at /transactions/add/."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/transactions/add/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test view is accessible by URL name 'transaction_create'."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test view uses the correct template."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_create'))
        self.assertTemplateUsed(response, 'transactions/transaction_form.html')

    def test_view_redirects_when_not_authenticated(self):
        """Test view redirects unauthenticated users to login."""
        response = self.client.get(reverse('transactions:transaction_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_view_post_creates_transaction(self):
        """Test POST request creates new transaction."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'category': self.category.id,
            'type': 'expense',
            'amount': '150.50',
            'date': date.today().strftime('%Y-%m-%d'),
            'note': 'Test transaction'
        }
        response = self.client.post(
            reverse('transactions:transaction_create'),
            data
        )

        # Should redirect after success
        self.assertEqual(response.status_code, 302)

        # Transaction should be created
        self.assertEqual(Transaction.objects.count(), 1)

        # Verify transaction data
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.type, 'expense')
        self.assertEqual(transaction.amount, Decimal('150.50'))
        self.assertEqual(transaction.note, 'Test transaction')

    def test_view_auto_sets_user_on_create(self):
        """Test view automatically sets user from request."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'category': self.category.id,
            'type': 'expense',
            'amount': '100.00',
            'date': date.today().strftime('%Y-%m-%d'),
        }
        self.client.post(reverse('transactions:transaction_create'), data)

        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)

    def test_view_redirects_to_transaction_list_after_create(self):
        """Test view redirects to transaction list after successful create."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'category': self.category.id,
            'type': 'expense',
            'amount': '100.00',
            'date': date.today().strftime('%Y-%m-%d'),
        }
        response = self.client.post(
            reverse('transactions:transaction_create'),
            data
        )
        self.assertRedirects(
            response,
            reverse('transactions:transaction_list')
        )

    def test_view_shows_errors_for_invalid_data(self):
        """Test view shows form errors for invalid data."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'category': self.category.id,
            'type': 'expense',
            'amount': '',  # Invalid: empty amount
            'date': date.today().strftime('%Y-%m-%d'),
        }
        response = self.client.post(
            reverse('transactions:transaction_create'),
            data
        )

        # Should not redirect (stays on form)
        self.assertEqual(response.status_code, 200)

        # Should not create transaction
        self.assertEqual(Transaction.objects.count(), 0)

        # Should have form with errors
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('amount', response.context['form'].errors)

    def test_view_requires_login_for_post(self):
        """Test POST request requires authentication."""
        data = {
            'category': self.category.id,
            'type': 'expense',
            'amount': '100.00',
            'date': date.today().strftime('%Y-%m-%d'),
        }
        response = self.client.post(
            reverse('transactions:transaction_create'),
            data
        )

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        # Should not create transaction
        self.assertEqual(Transaction.objects.count(), 0)


class TransactionUpdateViewTest(TestCase):
    """Test suite for TransactionUpdateView."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Food & Beverage',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today(),
            note='Original note'
        )

    def test_view_url_exists_at_desired_location(self):
        """Test view is accessible at /transactions/<id>/edit/."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/transactions/{self.transaction.id}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test view is accessible by URL name 'transaction_update'."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_update',
                    kwargs={'pk': self.transaction.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test view uses the correct template."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_update',
                    kwargs={'pk': self.transaction.id})
        )
        self.assertTemplateUsed(response, 'transactions/transaction_form.html')

    def test_view_redirects_when_not_authenticated(self):
        """Test view redirects or denies unauthenticated users."""
        response = self.client.get(
            reverse('transactions:transaction_update',
                    kwargs={'pk': self.transaction.id})
        )
        # Can be either 302 (redirect to login) or 403 (permission denied)
        self.assertIn(response.status_code, [302, 403])

    def test_view_denies_access_to_non_owner(self):
        """Test view denies access to users who don't own the transaction."""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_update',
                    kwargs={'pk': self.transaction.id})
        )

        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_view_allows_access_to_owner(self):
        """Test view allows access to transaction owner."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_update',
                    kwargs={'pk': self.transaction.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_post_updates_transaction(self):
        """Test POST request updates the transaction."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'category': self.category.id,
            'type': 'expense',
            'amount': '250.75',
            'date': date.today().strftime('%Y-%m-%d'),
            'note': 'Updated note'
        }
        response = self.client.post(
            reverse('transactions:transaction_update',
                    kwargs={'pk': self.transaction.id}),
            data
        )

        # Should redirect after success
        self.assertEqual(response.status_code, 302)

        # Transaction should be updated
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, Decimal('250.75'))
        self.assertEqual(self.transaction.note, 'Updated note')

    def test_view_denies_update_to_non_owner(self):
        """Test POST request denies update to non-owner."""
        self.client.login(username='otheruser', password='testpass123')
        data = {
            'category': self.category.id,
            'type': 'expense',
            'amount': '250.75',
            'date': date.today().strftime('%Y-%m-%d'),
            'note': 'Hacked note'
        }
        response = self.client.post(
            reverse('transactions:transaction_update',
                    kwargs={'pk': self.transaction.id}),
            data
        )

        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)

        # Transaction should not be updated
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, Decimal('100.00'))
        self.assertEqual(self.transaction.note, 'Original note')

    def test_view_redirects_to_transaction_list_after_update(self):
        """Test view redirects to transaction list after successful update."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'category': self.category.id,
            'type': 'expense',
            'amount': '150.00',
            'date': date.today().strftime('%Y-%m-%d'),
        }
        response = self.client.post(
            reverse('transactions:transaction_update',
                    kwargs={'pk': self.transaction.id}),
            data
        )
        self.assertRedirects(
            response,
            reverse('transactions:transaction_list')
        )

    def test_view_returns_404_for_nonexistent_transaction(self):
        """Test view returns 404 for nonexistent transaction."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_update', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)


class TransactionDeleteViewTest(TestCase):
    """Test suite for TransactionDeleteView."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Food & Beverage',
            type='expense',
            icon='🍔',
            color='#ef4444'
        )
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            type='expense',
            amount=Decimal('100.00'),
            date=date.today(),
            note='To be deleted'
        )

    def test_view_url_exists_at_desired_location(self):
        """Test view is accessible at /transactions/<id>/delete/."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/transactions/{self.transaction.id}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test view is accessible by URL name 'transaction_delete'."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_delete',
                    kwargs={'pk': self.transaction.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test view uses the correct template."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_delete',
                    kwargs={'pk': self.transaction.id})
        )
        self.assertTemplateUsed(
            response,
            'transactions/transaction_confirm_delete.html'
        )

    def test_view_redirects_when_not_authenticated(self):
        """Test view redirects or denies unauthenticated users."""
        response = self.client.get(
            reverse('transactions:transaction_delete',
                    kwargs={'pk': self.transaction.id})
        )
        # Can be either 302 (redirect to login) or 403 (permission denied)
        self.assertIn(response.status_code, [302, 403])

    def test_view_denies_access_to_non_owner(self):
        """Test view denies access to users who don't own the transaction."""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_delete',
                    kwargs={'pk': self.transaction.id})
        )

        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_view_allows_access_to_owner(self):
        """Test view allows access to transaction owner."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_delete',
                    kwargs={'pk': self.transaction.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_post_deletes_transaction(self):
        """Test POST request deletes the transaction."""
        self.client.login(username='testuser', password='testpass123')

        # Verify transaction exists
        self.assertEqual(Transaction.objects.count(), 1)

        response = self.client.post(
            reverse('transactions:transaction_delete',
                    kwargs={'pk': self.transaction.id})
        )

        # Should redirect after success
        self.assertEqual(response.status_code, 302)

        # Transaction should be deleted
        self.assertEqual(Transaction.objects.count(), 0)

    def test_view_denies_delete_to_non_owner(self):
        """Test POST request denies delete to non-owner."""
        self.client.login(username='otheruser', password='testpass123')

        response = self.client.post(
            reverse('transactions:transaction_delete',
                    kwargs={'pk': self.transaction.id})
        )

        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)

        # Transaction should not be deleted
        self.assertEqual(Transaction.objects.count(), 1)

    def test_view_redirects_to_transaction_list_after_delete(self):
        """Test view redirects to transaction list after successful delete."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('transactions:transaction_delete',
                    kwargs={'pk': self.transaction.id})
        )
        self.assertRedirects(
            response,
            reverse('transactions:transaction_list')
        )

    def test_view_returns_404_for_nonexistent_transaction(self):
        """Test view returns 404 for nonexistent transaction."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_delete', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)
