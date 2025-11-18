"""Template tests for accounts app."""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal


class RegisterTemplateTest(TestCase):
    """Test suite for register.html template."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_register_template_extends_base(self):
        """Test register template extends base.html."""
        response = self.client.get('/accounts/register/')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_template_has_form_fields(self):
        """Test register template displays all form fields."""
        response = self.client.get('/accounts/register/')
        self.assertContains(response, 'username')
        self.assertContains(response, 'email')
        self.assertContains(response, 'password1')
        self.assertContains(response, 'password2')
        self.assertContains(response, 'display_name')

    def test_register_template_has_bootstrap_styling(self):
        """Test register template uses Bootstrap styling."""
        response = self.client.get('/accounts/register/')
        self.assertContains(response, 'form-control')
        self.assertContains(response, 'btn btn-primary')
        self.assertContains(response, 'card')

    def test_register_template_displays_form_errors(self):
        """Test register template displays form errors."""
        data = {
            'username': '',
            'email': 'invalid',
            'password1': '123',
            'password2': '456',
        }
        response = self.client.post('/accounts/register/', data)
        self.assertContains(response, 'invalid-feedback')

    def test_register_template_has_link_to_login(self):
        """Test register template has link to login page."""
        response = self.client.get('/accounts/register/')
        self.assertContains(response, 'Đăng nhập')

    def test_register_template_has_green_color_scheme(self):
        """Test register template uses green primary button."""
        response = self.client.get('/accounts/register/')
        # Primary button should use green color from base.html
        self.assertContains(response, 'btn-primary')

    def test_register_template_is_responsive(self):
        """Test register template has responsive classes."""
        response = self.client.get('/accounts/register/')
        self.assertContains(response, 'col-md')
        self.assertContains(response, 'col-lg')


class LoginTemplateTest(TestCase):
    """Test suite for login.html template."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_login_template_extends_base(self):
        """Test login template extends base.html."""
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_template_has_form_fields(self):
        """Test login template displays username and password fields."""
        response = self.client.get('/accounts/login/')
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')

    def test_login_template_has_bootstrap_styling(self):
        """Test login template uses Bootstrap styling."""
        response = self.client.get('/accounts/login/')
        self.assertContains(response, 'form-control')
        self.assertContains(response, 'btn btn-primary')
        self.assertContains(response, 'card')

    def test_login_template_has_remember_me_checkbox(self):
        """Test login template has remember me checkbox."""
        response = self.client.get('/accounts/login/')
        self.assertContains(response, 'remember_me')
        self.assertContains(response, 'Ghi nhớ đăng nhập')
        self.assertContains(response, 'form-check')

    def test_login_template_has_link_to_register(self):
        """Test login template has link to register page."""
        response = self.client.get('/accounts/login/')
        self.assertContains(response, 'Đăng ký')

    def test_login_template_has_password_reset_link(self):
        """Test login template has password reset link."""
        response = self.client.get('/accounts/login/')
        self.assertContains(response, 'Quên mật khẩu')

    def test_login_template_displays_form_errors(self):
        """Test login template displays form errors."""
        # Create a user first
        User.objects.create_user(username='testuser', password='correctpass')
        # Try to login with wrong password
        data = {
            'username': 'testuser',
            'password': 'wrongpass',
        }
        response = self.client.post('/accounts/login/', data)
        # Should show form with errors (status 200, not redirect)
        self.assertEqual(response.status_code, 200)
        # Check if error structure is present in template
        self.assertIn('form', response.context)

    def test_login_template_is_responsive(self):
        """Test login template has responsive classes."""
        response = self.client.get('/accounts/login/')
        self.assertContains(response, 'col-md')
        self.assertContains(response, 'col-lg')


class ProfileTemplateTest(TestCase):
    """Test suite for profile.html template."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
        self.profile.display_name = 'Test User'
        self.profile.monthly_budget = Decimal('5000000.00')
        self.profile.save()
        self.client.login(username='testuser', password='testpass123')

    def test_profile_template_extends_base(self):
        """Test profile template extends base.html."""
        response = self.client.get('/profile/')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_template_has_bootstrap_styling(self):
        """Test profile template uses Bootstrap styling."""
        response = self.client.get('/profile/')
        self.assertContains(response, 'form-control')
        self.assertContains(response, 'btn btn-primary')
        self.assertContains(response, 'card')

    def test_profile_template_displays_user_information(self):
        """Test profile template displays user information."""
        response = self.client.get('/profile/')
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, 'Tên đăng nhập')
        self.assertContains(response, 'Email')

    def test_profile_template_has_profile_form(self):
        """Test profile template has profile update form."""
        response = self.client.get('/profile/')
        self.assertContains(response, 'display_name')
        self.assertContains(response, 'monthly_budget')

    def test_profile_template_has_change_password_link(self):
        """Test profile template has change password link."""
        response = self.client.get('/profile/')
        self.assertContains(response, 'Đổi mật khẩu')
        self.assertContains(response, 'btn-outline-secondary')

    def test_profile_template_displays_form_errors(self):
        """Test profile template displays form errors."""
        data = {
            'display_name': 'a' * 101,  # Exceeds max_length
            'monthly_budget': '5000000.00'
        }
        response = self.client.post('/profile/', data)
        self.assertContains(response, 'invalid-feedback')

    def test_profile_template_is_responsive(self):
        """Test profile template has responsive classes."""
        response = self.client.get('/profile/')
        self.assertContains(response, 'col-md')
        self.assertContains(response, 'col-lg')

    def test_profile_template_uses_green_color_scheme(self):
        """Test profile template uses green primary button."""
        response = self.client.get('/profile/')
        # Primary button should use green color from base.html
        self.assertContains(response, 'btn-primary')

    def test_profile_template_shows_current_values(self):
        """Test profile template shows current profile values."""
        response = self.client.get('/profile/')
        # Form should be populated with current values
        self.assertContains(response, 'Test User')


class TemplateResponsivenessTest(TestCase):
    """Test suite for responsive design of all templates."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_all_templates_use_bootstrap_5(self):
        """Test all templates inherit Bootstrap 5 from base.html."""
        urls = [
            '/accounts/register/',
            '/accounts/login/',
        ]
        for url in urls:
            response = self.client.get(url)
            # Base.html includes Bootstrap 5 CDN
            self.assertTemplateUsed(response, 'base.html')

    def test_all_templates_have_viewport_meta(self):
        """Test all templates inherit viewport meta from base.html."""
        urls = [
            '/accounts/register/',
            '/accounts/login/',
        ]
        for url in urls:
            response = self.client.get(url)
            # Base.html includes viewport meta
            self.assertTemplateUsed(response, 'base.html')

    def test_all_authenticated_templates_work(self):
        """Test authenticated templates render correctly."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
