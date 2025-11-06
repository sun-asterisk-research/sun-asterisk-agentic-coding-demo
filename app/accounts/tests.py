"""Tests for accounts app."""
from django.test import TestCase
from django.contrib.auth.models import User


class RegisterFormTest(TestCase):
    """Test RegisterForm."""

    def test_valid_registration_form(self):
        """Test form with valid data."""
        from accounts.forms import RegisterForm
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        """Test form with mismatched passwords."""
        from accounts.forms import RegisterForm
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass123!',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_duplicate_username(self):
        """Test form with existing username."""
        from accounts.forms import RegisterForm
        
        # Create existing user
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com'
        )
        
        form_data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_invalid_email(self):
        """Test form with invalid email."""
        from accounts.forms import RegisterForm
        
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_weak_password(self):
        """Test form with weak password."""
        from accounts.forms import RegisterForm
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': '123',
            'password2': '123',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class RegisterViewTest(TestCase):
    """Test RegisterView."""

    def test_register_view_get(self):
        """Test GET request to register view."""
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_valid(self):
        """Test POST with valid registration data."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        response = self.client.post('/register/', data=form_data)
        
        # Should redirect after successful registration
        self.assertEqual(response.status_code, 302)
        
        # User should be created
        self.assertTrue(
            User.objects.filter(username='newuser').exists()
        )
        
        # User should be logged in
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')

    def test_register_view_post_invalid(self):
        """Test POST with invalid data."""
        form_data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': '123',
            'password2': '456',
        }
        response = self.client.post('/register/', data=form_data)
        
        # Should not redirect (stays on form)
        self.assertEqual(response.status_code, 200)
        
        # User should not be created
        self.assertFalse(
            User.objects.filter(username='newuser').exists()
        )


class LoginViewTest(TestCase):
    """Test LoginView."""

    def setUp(self):
        """Setup test user."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_view_get(self):
        """Test GET request to login view."""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_valid(self):
        """Test POST with valid credentials."""
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123',
        })
        
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/dashboard/')

    def test_login_view_post_invalid(self):
        """Test POST with invalid credentials."""
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        
        # Should not redirect
        self.assertEqual(response.status_code, 200)
        
        # Should show error message
        self.assertContains(response, 'không đúng')


class LogoutViewTest(TestCase):
    """Test LogoutView."""

    def setUp(self):
        """Setup test user."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_logout_view(self):
        """Test logout functionality."""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Then logout
        response = self.client.get('/logout/')
        
        # Should redirect to home
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
