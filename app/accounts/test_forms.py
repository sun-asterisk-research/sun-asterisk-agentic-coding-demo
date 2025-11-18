from django.test import TestCase
from django.contrib.auth.models import User
from django.forms import PasswordInput, EmailInput


class UserRegistrationFormTest(TestCase):
    """Test suite for UserRegistrationForm."""

    def test_form_has_required_fields(self):
        """Test form includes all required fields."""
        from accounts.forms import UserRegistrationForm

        form = UserRegistrationForm()
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        self.assertIn('display_name', form.fields)

    def test_form_field_labels(self):
        """Test form fields have correct labels."""
        from accounts.forms import UserRegistrationForm

        form = UserRegistrationForm()
        self.assertEqual(form.fields['username'].label, 'Tên đăng nhập')
        self.assertEqual(form.fields['email'].label, 'Email')
        self.assertEqual(form.fields['password1'].label, 'Mật khẩu')
        self.assertEqual(form.fields['password2'].label, 'Xác nhận mật khẩu')
        self.assertEqual(form.fields['display_name'].label, 'Tên hiển thị')

    def test_display_name_field_is_optional(self):
        """Test display_name field is not required."""
        from accounts.forms import UserRegistrationForm

        form = UserRegistrationForm()
        self.assertFalse(form.fields['display_name'].required)

    def test_username_email_password_fields_are_required(self):
        """Test username, email, and password fields are required."""
        from accounts.forms import UserRegistrationForm

        form = UserRegistrationForm()
        self.assertTrue(form.fields['username'].required)
        self.assertTrue(form.fields['email'].required)
        self.assertTrue(form.fields['password1'].required)
        self.assertTrue(form.fields['password2'].required)

    def test_form_valid_with_correct_data(self):
        """Test form is valid with correct data."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_without_display_name(self):
        """Test form is valid when display_name is not provided."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_missing_username(self):
        """Test form is invalid when username is missing."""
        from accounts.forms import UserRegistrationForm

        data = {
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_invalid_with_missing_email(self):
        """Test form is invalid when email is missing."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_invalid_with_missing_password1(self):
        """Test form is invalid when password1 is missing."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password2': 'SecurePass123!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_form_invalid_with_missing_password2(self):
        """Test form is invalid when password2 is missing."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_invalid_with_empty_username(self):
        """Test form is invalid with empty username."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': '',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_invalid_with_invalid_email_format(self):
        """Test form is invalid with incorrect email format."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_invalid_with_empty_email(self):
        """Test form is invalid with empty email."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': '',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_invalid_when_passwords_do_not_match(self):
        """Test form is invalid when password1 and password2 don't match."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass456!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_invalid_with_weak_password(self):
        """Test form is invalid with weak password (too short)."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'weak',
            'password2': 'weak',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_invalid_with_common_password(self):
        """Test form is invalid with commonly used password."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_invalid_with_numeric_only_password(self):
        """Test form is invalid with numeric-only password."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': '123456789',
            'password2': '123456789',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_invalid_with_username_too_similar_to_password(self):
        """Test form is invalid when password is too similar to username."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testuser123',
            'password2': 'testuser123',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_invalid_with_duplicate_username(self):
        """Test form is invalid when username already exists."""
        from accounts.forms import UserRegistrationForm

        # Create existing user
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='SecurePass123!'
        )

        # Try to create user with same username
        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'New User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_saves_user_with_valid_data(self):
        """Test form save method creates User with valid data."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'New User'
        }
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

        user = form.save()

        # Verify user was created
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('SecurePass123!'))

    def test_form_saves_user_and_creates_profile(self):
        """Test form save creates User and UserProfile is auto-created."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'profileuser',
            'email': 'profile@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'Profile User'
        }
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

        user = form.save()

        # Verify UserProfile was created automatically
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.user, user)

    def test_form_saves_display_name_to_profile(self):
        """Test form save method sets display_name in UserProfile."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'displayuser',
            'email': 'display@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'Display Name User'
        }
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

        user = form.save()

        # Verify display_name was saved to profile
        self.assertEqual(user.profile.display_name, 'Display Name User')

    def test_form_saves_without_display_name(self):
        """Test form save works when display_name is not provided."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'nodisplayuser',
            'email': 'nodisplay@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

        user = form.save()

        # Verify user and profile created, display_name is empty
        self.assertIsNotNone(user.id)
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.display_name, '')

    def test_form_field_help_texts(self):
        """Test form fields have appropriate help texts."""
        from accounts.forms import UserRegistrationForm

        form = UserRegistrationForm()

        # Check username help text
        self.assertIsNotNone(form.fields['username'].help_text)

        # Check password help text
        self.assertIsNotNone(form.fields['password1'].help_text)

    def test_form_username_field_max_length(self):
        """Test username field respects max_length."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'a' * 151,  # Django User username max_length is 150
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_display_name_field_max_length(self):
        """Test display_name field respects max_length of 100."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'a' * 101
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('display_name', form.errors)

    def test_form_accepts_valid_display_name_length(self):
        """Test display_name accepts string up to 100 characters."""
        from accounts.forms import UserRegistrationForm

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'a' * 100
        }
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_email_field_accepts_valid_email(self):
        """Test email field accepts various valid email formats."""
        from accounts.forms import UserRegistrationForm

        valid_emails = [
            'test@example.com',
            'user.name@example.com',
            'user+tag@example.co.uk',
            'user123@test-domain.com'
        ]

        for idx, email in enumerate(valid_emails):
            data = {
                'username': f'testuser{idx}',
                'email': email,
                'password1': 'SecurePass123!',
                'password2': 'SecurePass123!',
                'display_name': 'Test User'
            }
            form = UserRegistrationForm(data=data)
            self.assertTrue(
                form.is_valid(),
                f"Form should be valid with email: {email}"
            )

    def test_form_username_field_alphanumeric_validation(self):
        """Test username field accepts valid characters."""
        from accounts.forms import UserRegistrationForm

        # Valid username with alphanumeric and underscore
        data = {
            'username': 'test_user123',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'display_name': 'Test User'
        }
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_password_gets_hashed_on_save(self):
        """Test password is properly hashed when user is saved."""
        from accounts.forms import UserRegistrationForm

        password = 'SecurePass123!'
        data = {
            'username': 'hashuser',
            'email': 'hash@example.com',
            'password1': password,
            'password2': password,
            'display_name': 'Hash User'
        }
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

        user = form.save()

        # Password should be hashed, not stored in plaintext
        self.assertNotEqual(user.password, password)
        # But check_password should work
        self.assertTrue(user.check_password(password))

    def test_form_widget_types(self):
        """Test form fields use appropriate widget types."""
        from accounts.forms import UserRegistrationForm

        form = UserRegistrationForm()

        # Password fields should use PasswordInput widget
        self.assertIsInstance(
            form.fields['password1'].widget,
            PasswordInput
        )
        self.assertIsInstance(
            form.fields['password2'].widget,
            PasswordInput
        )

        # Email field should use EmailInput widget
        self.assertIsInstance(
            form.fields['email'].widget,
            EmailInput
        )


class UserProfileFormTest(TestCase):
    """Test suite for UserProfileForm."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile

    def test_form_has_required_fields(self):
        """Test form includes all required fields."""
        from accounts.forms import UserProfileForm

        form = UserProfileForm()
        self.assertIn('display_name', form.fields)
        self.assertIn('monthly_budget', form.fields)

    def test_form_fields_are_optional(self):
        """Test both fields are optional."""
        from accounts.forms import UserProfileForm

        form = UserProfileForm()
        self.assertFalse(form.fields['display_name'].required)
        self.assertFalse(form.fields['monthly_budget'].required)

    def test_form_valid_with_both_fields(self):
        """Test form is valid with both fields populated."""
        from accounts.forms import UserProfileForm
        from decimal import Decimal

        data = {
            'display_name': 'Test Display Name',
            'monthly_budget': '5000000.00'
        }
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_only_display_name(self):
        """Test form is valid with only display_name."""
        from accounts.forms import UserProfileForm

        data = {
            'display_name': 'Test Name',
            'monthly_budget': ''
        }
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_only_monthly_budget(self):
        """Test form is valid with only monthly_budget."""
        from accounts.forms import UserProfileForm

        data = {
            'display_name': '',
            'monthly_budget': '3000000.50'
        }
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_empty_fields(self):
        """Test form is valid with all empty fields."""
        from accounts.forms import UserProfileForm

        data = {
            'display_name': '',
            'monthly_budget': ''
        }
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_negative_budget(self):
        """Test form is invalid with negative monthly_budget."""
        from accounts.forms import UserProfileForm

        data = {
            'display_name': 'Test',
            'monthly_budget': '-1000.00'
        }
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('monthly_budget', form.errors)

    def test_form_invalid_with_invalid_budget_format(self):
        """Test form is invalid with non-decimal monthly_budget."""
        from accounts.forms import UserProfileForm

        data = {
            'display_name': 'Test',
            'monthly_budget': 'invalid'
        }
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('monthly_budget', form.errors)

    def test_form_display_name_max_length(self):
        """Test display_name respects max_length."""
        from accounts.forms import UserProfileForm

        data = {
            'display_name': 'a' * 101,
            'monthly_budget': '1000000.00'
        }
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('display_name', form.errors)

    def test_form_accepts_valid_display_name_length(self):
        """Test display_name accepts string up to 100 characters."""
        from accounts.forms import UserProfileForm

        data = {
            'display_name': 'a' * 100,
            'monthly_budget': '1000000.00'
        }
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_saves_profile_correctly(self):
        """Test form save method updates profile."""
        from accounts.forms import UserProfileForm
        from decimal import Decimal

        data = {
            'display_name': 'Updated Name',
            'monthly_budget': '7000000.00'
        }
        form = UserProfileForm(data=data, instance=self.profile)
        self.assertTrue(form.is_valid())

        updated_profile = form.save()

        # Verify profile was updated
        self.assertEqual(updated_profile.display_name, 'Updated Name')
        self.assertEqual(updated_profile.monthly_budget, Decimal('7000000.00'))

    def test_form_field_labels(self):
        """Test form fields have correct Vietnamese labels."""
        from accounts.forms import UserProfileForm

        form = UserProfileForm()
        self.assertEqual(form.fields['display_name'].label, 'Tên hiển thị')
        self.assertEqual(form.fields['monthly_budget'].label, 'Ngân sách tháng')

    def test_form_monthly_budget_help_text(self):
        """Test monthly_budget has appropriate help text."""
        from accounts.forms import UserProfileForm

        form = UserProfileForm()
        self.assertIsNotNone(form.fields['monthly_budget'].help_text)
        self.assertIn('VND', form.fields['monthly_budget'].help_text)

    def test_form_accepts_large_budget_values(self):
        """Test form accepts large decimal values for budget."""
        from accounts.forms import UserProfileForm
        from decimal import Decimal

        data = {
            'display_name': 'Rich User',
            'monthly_budget': '9999999999.99'
        }
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_accepts_zero_budget(self):
        """Test form accepts zero as valid budget."""
        from accounts.forms import UserProfileForm
        from decimal import Decimal

        data = {
            'display_name': 'Zero Budget',
            'monthly_budget': '0.00'
        }
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())
