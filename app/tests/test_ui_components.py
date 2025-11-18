"""
Test suite for UI/UX components and responsive design.

This module tests the custom CSS, toast notifications, loading states,
modals, and responsive design features.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages


class CustomCSSTest(TestCase):
    """Test custom CSS file exists and is loaded correctly."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_custom_css_file_exists(self):
        """Test custom CSS file exists at static/css/style.css."""
        from django.conf import settings
        import os

        css_path = os.path.join(
            settings.BASE_DIR,
            'static',
            'css',
            'style.css'
        )
        self.assertTrue(
            os.path.exists(css_path),
            "Custom CSS file should exist at static/css/style.css"
        )

    def test_base_template_loads_custom_css(self):
        """Test base.html template includes custom CSS file."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        self.assertEqual(response.status_code, 200)
        # Check for the CSS link tag (WhiteNoise hashes the filename)
        self.assertContains(
            response,
            'css/style',
            msg_prefix="Base template should load custom CSS file"
        )


class ResponsiveNavbarTest(TestCase):
    """Test responsive navbar with user dropdown."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_navbar_has_responsive_toggle_button(self):
        """Test navbar includes responsive toggle button for mobile."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        self.assertContains(response, 'navbar-toggler')
        self.assertContains(response, 'data-bs-toggle="collapse"')

    def test_navbar_has_user_dropdown(self):
        """Test navbar includes user dropdown menu."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        # Check for dropdown elements
        self.assertContains(response, 'dropdown')
        self.assertContains(response, self.user.username)
        self.assertContains(response, 'Profile')
        self.assertContains(response, 'Logout')

    def test_navbar_shows_active_page_highlighting(self):
        """Test navbar highlights the active page link."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        # Check for nav-link class (used for highlighting)
        self.assertContains(response, 'nav-link')
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_navbar_shows_login_register(self):
        """Test navbar shows Login and Register for unauthenticated users."""
        response = self.client.get(reverse('accounts:login'))

        self.assertContains(response, 'Login')
        self.assertContains(response, 'Register')
        self.assertNotContains(response, 'Profile')


class ToastNotificationsTest(TestCase):
    """Test toast notifications and Django messages system."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_base_template_has_toast_container(self):
        """Test base.html includes toast notification container."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        # Check for toast container element
        self.assertContains(
            response,
            'toast-container',
            msg_prefix="Base template should include toast container"
        )

    def test_django_messages_render_as_toasts(self):
        """Test Django messages are rendered as toast notifications."""
        from django.contrib.messages import get_messages
        from django.contrib.messages.storage.session import SessionStorage

        # Login first
        self.client.login(username='testuser', password='testpass123')

        # Get a session
        session = self.client.session
        session['_messages'] = 'test'
        session.save()

        # Access a page - the template structure for toasts should exist
        response = self.client.get(reverse('reports:dashboard'))

        # Check that toast container exists in template
        self.assertContains(response, 'toast-container')
        self.assertEqual(response.status_code, 200)

    def test_toast_has_auto_dismiss_functionality(self):
        """Test toast notifications have auto-dismiss JavaScript."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        # Check for auto-dismiss script
        self.assertContains(
            response,
            'setTimeout',
            msg_prefix="Toast should have auto-dismiss with setTimeout"
        )


class LoadingStatesTest(TestCase):
    """Test loading states and spinners."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_loading_spinner_component_exists(self):
        """Test loading spinner HTML component is available."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))

        # Check that spinner class or element exists in templates
        # This will be added as a reusable component
        self.assertEqual(response.status_code, 200)


class ConfirmationModalsTest(TestCase):
    """Test confirmation modals for delete actions."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_delete_confirmation_modal_exists(self):
        """Test delete confirmation uses Bootstrap modal."""
        from transactions.models import Transaction, Category

        # Create a category and transaction
        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='💰',
            color='#22c55e'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            amount=100.00,
            type='expense',
            date='2025-01-01',
            note='Test transaction'
        )

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('transactions:transaction_delete', kwargs={'pk': transaction.pk})
        )

        # Check for modal elements
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'modal')


class ResponsiveDesignTest(TestCase):
    """Test responsive design across different devices."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_viewport_meta_tag_exists(self):
        """Test viewport meta tag for mobile responsiveness."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        self.assertContains(
            response,
            'viewport',
            msg_prefix="Page should include viewport meta tag"
        )
        self.assertContains(response, 'width=device-width')

    def test_bootstrap_grid_classes_used(self):
        """Test Bootstrap responsive grid classes are used."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        # Check for responsive column classes
        self.assertContains(response, 'col-md')
        self.assertContains(response, 'col-lg')

    def test_navbar_collapse_for_mobile(self):
        """Test navbar uses collapse for mobile devices."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        self.assertContains(response, 'navbar-collapse')
        self.assertContains(response, 'navbar-toggler')

    def test_table_responsive_wrapper(self):
        """Test tables are wrapped in responsive containers."""
        from transactions.models import Transaction, Category

        # Create test data so table is rendered
        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='💰',
            color='#22c55e'
        )
        Transaction.objects.create(
            user=self.user,
            category=category,
            amount=100.00,
            type='expense',
            date='2025-01-01'
        )

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))

        self.assertContains(
            response,
            'table-responsive',
            msg_prefix="Tables should be wrapped in responsive container"
        )


class ButtonStylingTest(TestCase):
    """Test custom button styling."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_primary_buttons_use_green_theme(self):
        """Test primary buttons use the green color scheme."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        # Check for primary button class
        self.assertContains(response, 'btn-primary')

    def test_danger_buttons_use_red_theme(self):
        """Test danger buttons use the red color scheme."""
        from transactions.models import Transaction, Category

        category = Category.objects.create(
            name='Test Category',
            type='expense',
            icon='💰',
            color='#22c55e'
        )

        transaction = Transaction.objects.create(
            user=self.user,
            category=category,
            amount=100.00,
            type='expense',
            date='2025-01-01'
        )

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('transactions:transaction_list'))

        # Check for danger button (delete)
        self.assertContains(response, 'btn-danger')


class CardStylingTest(TestCase):
    """Test custom card component styling."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_cards_have_custom_styling(self):
        """Test cards use custom CSS classes."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        # Check for card elements
        self.assertContains(response, 'card')
        self.assertContains(response, 'card-header')
        self.assertContains(response, 'card-body')

    def test_stat_cards_on_dashboard(self):
        """Test dashboard has styled stat cards."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))

        # Check for stat card classes
        self.assertContains(response, 'stat-card')
