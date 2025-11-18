from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from decimal import Decimal
from accounts.models import UserProfile


class UserProfileModelTest(TestCase):
    """Test suite for UserProfile model."""

    def setUp(self):
        """Set up test data that's needed for multiple tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Profile is auto-created by signal, just update it
        self.profile = self.user.profile
        self.profile.display_name = 'Test User'
        self.profile.save()

    def test_user_profile_creation(self):
        """Test UserProfile instance can be created with valid data."""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.display_name, 'Test User')
        self.assertIsNotNone(self.profile.id)
        self.assertIsNotNone(self.profile.created_at)
        self.assertIsNotNone(self.profile.updated_at)

    def test_str_representation(self):
        """Test __str__ method returns expected string format."""
        expected = f"Profile of {self.user.username}"
        self.assertEqual(str(self.profile), expected)

    def test_one_to_one_relationship_with_user(self):
        """Test OneToOne relationship with User model."""
        # Access profile from user
        self.assertEqual(self.user.profile, self.profile)
        # Access user from profile
        self.assertEqual(self.profile.user, self.user)

    def test_user_can_only_have_one_profile(self):
        """Test that one user can only have one profile (OneToOne constraint)."""
        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(
                user=self.user,
                display_name='Duplicate Profile'
            )

    def test_display_name_field(self):
        """Test display_name field accepts valid strings."""
        user = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        # Profile is auto-created by signal
        profile = user.profile
        profile.display_name = 'John Doe'
        profile.save()
        self.assertEqual(profile.display_name, 'John Doe')

    def test_display_name_can_be_blank(self):
        """Test display_name field can be blank."""
        user = User.objects.create_user(
            username='user3',
            password='pass123'
        )
        # Profile is auto-created by signal
        profile = user.profile
        profile.display_name = ''
        profile.save()
        self.assertEqual(profile.display_name, '')
        profile.full_clean()  # Should not raise ValidationError

    def test_display_name_max_length(self):
        """Test display_name field respects max_length of 100."""
        long_name = 'a' * 101
        profile = UserProfile(
            user=User.objects.create_user(
                username='user4',
                password='pass123'
            ),
            display_name=long_name
        )
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_avatar_field_is_optional(self):
        """Test avatar field can be null/blank."""
        user = User.objects.create_user(
            username='user5',
            password='pass123'
        )
        # Profile is auto-created by signal
        profile = user.profile
        profile.display_name = 'User Without Avatar'
        profile.save()
        self.assertIsNone(profile.avatar.name)
        self.assertFalse(profile.avatar)

    def test_monthly_budget_field_is_optional(self):
        """Test monthly_budget field can be null/blank."""
        user = User.objects.create_user(
            username='user6',
            password='pass123'
        )
        # Profile is auto-created by signal
        profile = user.profile
        profile.display_name = 'User Without Budget'
        profile.save()
        self.assertIsNone(profile.monthly_budget)

    def test_monthly_budget_accepts_decimal_values(self):
        """Test monthly_budget field accepts valid decimal values."""
        user = User.objects.create_user(
            username='user7',
            password='pass123'
        )
        # Profile is auto-created by signal
        profile = user.profile
        profile.display_name = 'User With Budget'
        profile.monthly_budget = Decimal('5000000.00')
        profile.save()
        self.assertEqual(profile.monthly_budget, Decimal('5000000.00'))

    def test_monthly_budget_precision(self):
        """Test monthly_budget field stores values with correct precision."""
        user = User.objects.create_user(
            username='user8',
            password='pass123'
        )
        # Profile is auto-created by signal
        profile = user.profile
        profile.display_name = 'Precision Test'
        profile.monthly_budget = Decimal('10000000.50')
        profile.save()
        self.assertEqual(profile.monthly_budget, Decimal('10000000.50'))

    def test_cascade_delete_when_user_deleted(self):
        """Test profile is deleted when user is deleted (CASCADE)."""
        user = User.objects.create_user(
            username='deleteme',
            password='pass123'
        )
        # Profile is auto-created by signal
        profile = user.profile
        profile.display_name = 'To Be Deleted'
        profile.save()
        profile_id = profile.id

        user.delete()

        # Profile should no longer exist
        self.assertFalse(UserProfile.objects.filter(id=profile_id).exists())

    def test_related_name_is_profile(self):
        """Test related_name 'profile' allows access from User."""
        user = User.objects.create_user(
            username='relatedtest',
            password='pass123'
        )
        # Profile is auto-created by signal
        profile = user.profile
        profile.display_name = 'Related Name Test'
        profile.save()

        # Should be accessible via user.profile
        self.assertEqual(user.profile, profile)

    def test_created_at_auto_now_add(self):
        """Test created_at is automatically set on creation."""
        user = User.objects.create_user(
            username='timetest1',
            password='pass123'
        )
        # Profile is auto-created by signal
        profile = user.profile
        profile.display_name = 'Time Test'
        profile.save()
        self.assertIsNotNone(profile.created_at)

    def test_updated_at_auto_now(self):
        """Test updated_at is automatically updated on save."""
        user = User.objects.create_user(
            username='timetest2',
            password='pass123'
        )
        # Profile is auto-created by signal
        profile = user.profile
        profile.display_name = 'Update Test'
        profile.save()
        original_updated_at = profile.updated_at

        # Update the profile
        profile.display_name = 'Updated Name'
        profile.save()

        # updated_at should be different (greater than original)
        self.assertGreater(profile.updated_at, original_updated_at)

    def test_verbose_names(self):
        """Test model and field verbose names are set correctly."""
        self.assertEqual(
            UserProfile._meta.verbose_name,
            'Hồ sơ người dùng'
        )
        self.assertEqual(
            UserProfile._meta.verbose_name_plural,
            'Hồ sơ người dùng'
        )

    def test_user_field_verbose_name(self):
        """Test user field has correct verbose_name."""
        user_field = UserProfile._meta.get_field('user')
        self.assertEqual(user_field.verbose_name, 'Người dùng')

    def test_display_name_field_verbose_name(self):
        """Test display_name field has correct verbose_name."""
        display_name_field = UserProfile._meta.get_field('display_name')
        self.assertEqual(display_name_field.verbose_name, 'Tên hiển thị')

    def test_avatar_field_verbose_name(self):
        """Test avatar field has correct verbose_name."""
        avatar_field = UserProfile._meta.get_field('avatar')
        self.assertEqual(avatar_field.verbose_name, 'Ảnh đại diện')

    def test_monthly_budget_field_verbose_name_and_help_text(self):
        """Test monthly_budget field has correct verbose_name and help_text."""
        monthly_budget_field = UserProfile._meta.get_field('monthly_budget')
        self.assertEqual(monthly_budget_field.verbose_name, 'Ngân sách tháng')
        self.assertEqual(
            monthly_budget_field.help_text,
            'Giới hạn chi tiêu hàng tháng'
        )

    def test_avatar_upload_path(self):
        """Test avatar field has correct upload_to path."""
        avatar_field = UserProfile._meta.get_field('avatar')
        self.assertEqual(avatar_field.upload_to, 'avatars/')


class UserProfileSignalTest(TestCase):
    """Test suite for UserProfile signal auto-creation."""

    def test_user_profile_created_automatically_on_user_creation(self):
        """Test UserProfile is created automatically when a new User is created."""
        # Create a new user
        user = User.objects.create_user(
            username='signaltest',
            email='signal@test.com',
            password='testpass123'
        )

        # UserProfile should be created automatically
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.user, user)

    def test_user_profile_not_duplicated_on_user_save(self):
        """Test UserProfile is not duplicated when user is saved again."""
        # Create a new user (profile should be auto-created)
        user = User.objects.create_user(
            username='savetest',
            email='save@test.com',
            password='testpass123'
        )

        # Get the profile
        profile = user.profile
        profile_id = profile.id

        # Update user and save again
        user.email = 'newemail@test.com'
        user.save()

        # Profile should still be the same
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)
        self.assertEqual(user.profile.id, profile_id)

    def test_user_profile_created_for_superuser(self):
        """Test UserProfile is created for superusers as well."""
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )

        # UserProfile should be created automatically
        self.assertTrue(hasattr(superuser, 'profile'))
        self.assertIsNotNone(superuser.profile)
        self.assertEqual(superuser.profile.user, superuser)

    def test_signal_handles_existing_user_with_profile(self):
        """Test signal doesn't fail when user already has a profile."""
        # Manually create user and profile
        user = User.objects.create_user(
            username='existingprofile',
            email='existing@test.com',
            password='testpass123'
        )

        # Profile should already exist from signal
        original_profile = user.profile
        original_profile_id = original_profile.id

        # Update and save user again
        user.first_name = 'Test'
        user.save()

        # Should still have only one profile
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)
        self.assertEqual(user.profile.id, original_profile_id)


class UserProfileAdminTest(TestCase):
    """Test suite for UserProfile admin registration."""

    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Profile should be auto-created via signal
        self.profile = self.regular_user.profile
        self.profile.display_name = 'Test User'
        self.profile.monthly_budget = Decimal('5000000.00')
        self.profile.save()

    def test_userprofile_admin_is_registered(self):
        """Test UserProfile model is registered with admin site."""
        from django.contrib import admin
        from accounts.models import UserProfile

        self.assertIn(UserProfile, admin.site._registry)

    def test_userprofile_admin_list_display(self):
        """Test UserProfileAdmin has correct list_display fields."""
        from django.contrib import admin
        from accounts.models import UserProfile

        userprofile_admin = admin.site._registry[UserProfile]
        expected_list_display = (
            'user', 'display_name', 'formatted_budget', 'user_email', 'date_joined'
        )

        self.assertEqual(
            userprofile_admin.list_display,
            expected_list_display
        )

    def test_userprofile_admin_search_fields(self):
        """Test UserProfileAdmin has correct search_fields."""
        from django.contrib import admin
        from accounts.models import UserProfile

        userprofile_admin = admin.site._registry[UserProfile]
        expected_search_fields = ('user__username', 'user__email', 'display_name')

        self.assertEqual(
            userprofile_admin.search_fields,
            expected_search_fields
        )


class RegisterViewTest(TestCase):
    """Test suite for RegisterView."""

    def setUp(self):
        """Set up test client and test data."""
        from django.test import Client
        self.client = Client()
        self.register_url = '/accounts/register/'
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }

    def test_register_view_url_exists_at_desired_location(self):
        """Test register view is accessible at expected URL."""
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_view_url_accessible_by_name(self):
        """Test register view is accessible by URL name."""
        from django.urls import reverse
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_uses_correct_template(self):
        """Test register view uses the correct template."""
        from django.urls import reverse
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_get_shows_registration_form(self):
        """Test GET request shows registration form with all fields."""
        from django.urls import reverse
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username')
        self.assertContains(response, 'email')
        self.assertContains(response, 'password1')
        self.assertContains(response, 'password2')

    def test_register_view_post_with_valid_data_creates_user(self):
        """Test POST with valid data creates new user."""
        from django.urls import reverse
        response = self.client.post(
            reverse('accounts:register'),
            data=self.valid_data
        )
        # Should create user
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')

    def test_register_view_post_with_valid_data_redirects_to_login(self):
        """Test POST with valid data redirects to login page."""
        from django.urls import reverse
        response = self.client.post(
            reverse('accounts:register'),
            data=self.valid_data
        )
        # Should redirect to login after successful registration
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_register_view_post_auto_creates_userprofile_via_signal(self):
        """Test UserProfile is auto-created via signal when user registers."""
        from django.urls import reverse
        response = self.client.post(
            reverse('accounts:register'),
            data=self.valid_data
        )
        # User should be created
        user = User.objects.get(username='newuser')
        # UserProfile should be auto-created via signal
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.user, user)

    def test_register_view_post_with_invalid_data_shows_errors(self):
        """Test POST with invalid data shows validation errors."""
        from django.urls import reverse
        invalid_data = {
            'username': '',  # Empty username
            'email': 'invalid-email',  # Invalid email format
            'password1': '123',  # Too short password
            'password2': '456',  # Mismatched password
        }
        response = self.client.post(
            reverse('accounts:register'),
            data=invalid_data
        )
        # Should not create user
        self.assertEqual(User.objects.count(), 0)
        # Should return 200 (form with errors)
        self.assertEqual(response.status_code, 200)
        # Should show form errors
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_register_view_post_with_mismatched_passwords_shows_error(self):
        """Test POST with mismatched passwords shows error."""
        from django.urls import reverse
        data = self.valid_data.copy()
        data['password2'] = 'DifferentPassword123!'
        response = self.client.post(reverse('accounts:register'), data=data)
        # Should not create user
        self.assertEqual(User.objects.count(), 0)
        # Should return 200 (form with errors)
        self.assertEqual(response.status_code, 200)
        # Should show password mismatch error
        self.assertFormError(
            response,
            'form',
            'password2',
            "The two password fields didn't match."
        )

    def test_register_view_post_with_duplicate_username_shows_error(self):
        """Test POST with duplicate username shows error."""
        from django.urls import reverse
        # Create existing user
        User.objects.create_user(
            username='newuser',
            email='existing@example.com',
            password='ExistingPass123!'
        )
        # Try to register with same username
        response = self.client.post(
            reverse('accounts:register'),
            data=self.valid_data
        )
        # Should not create another user
        self.assertEqual(User.objects.count(), 1)
        # Should return 200 (form with errors)
        self.assertEqual(response.status_code, 200)
        # Should show username already exists error
        self.assertFormError(
            response,
            'form',
            'username',
            'A user with that username already exists.'
        )

    def test_register_view_post_with_weak_password_shows_error(self):
        """Test POST with weak password shows validation error."""
        from django.urls import reverse
        data = self.valid_data.copy()
        data['password1'] = '123'
        data['password2'] = '123'
        response = self.client.post(reverse('accounts:register'), data=data)
        # Should not create user
        self.assertEqual(User.objects.count(), 0)
        # Should return 200 (form with errors)
        self.assertEqual(response.status_code, 200)
        # Should show password validation errors
        self.assertTrue(response.context['form'].errors.get('password2'))

    def test_register_view_redirects_authenticated_user(self):
        """Test authenticated users are redirected away from register page."""
        from django.urls import reverse
        # Create and login user
        user = User.objects.create_user(
            username='existinguser',
            password='testpass123'
        )
        self.client.login(username='existinguser', password='testpass123')
        # Try to access register page
        response = self.client.get(reverse('accounts:register'))
        # Should redirect (already logged in)
        self.assertEqual(response.status_code, 302)
        # Should redirect to dashboard or home
        self.assertTrue(
            response.url in ['/', '/dashboard/'] or
            response.url.startswith('/accounts/login/')
        )

    def test_register_view_form_context_is_provided(self):
        """Test register view provides form in context."""
        from django.urls import reverse
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsNotNone(response.context['form'])

    def test_register_view_post_with_invalid_email_shows_error(self):
        """Test POST with invalid email format shows error."""
        from django.urls import reverse
        data = self.valid_data.copy()
        data['email'] = 'not-an-email'
        response = self.client.post(reverse('accounts:register'), data=data)
        # Should not create user
        self.assertEqual(User.objects.count(), 0)
        # Should return 200 (form with errors)
        self.assertEqual(response.status_code, 200)
        # Should have form errors
        self.assertTrue(response.context['form'].errors)

    def test_register_view_post_success_message_displayed(self):
        """Test success message is displayed after successful registration."""
        from django.urls import reverse
        from django.contrib.messages import get_messages
        response = self.client.post(
            reverse('accounts:register'),
            data=self.valid_data,
            follow=True
        )
        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(len(messages) > 0)
        # Should contain success message about registration
        success_messages = [str(m) for m in messages if m.level_tag == 'success']
        self.assertTrue(len(success_messages) > 0)


class ProfileViewTest(TestCase):
    """Test suite for ProfileView."""

    def setUp(self):
        """Set up test client and test data."""
        from django.test import Client
        self.client = Client()

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Profile should be auto-created via signal
        self.profile = self.user.profile
        self.profile.display_name = 'Original Name'
        self.profile.monthly_budget = Decimal('3000000.00')
        self.profile.save()

        # Define profile URL
        self.profile_url = '/profile/'

    def test_profile_view_url_exists_at_desired_location(self):
        """Test profile view is accessible at /profile/ URL."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_profile_view_url_accessible_by_name(self):
        """Test profile view is accessible by URL name."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_uses_correct_template(self):
        """Test profile view uses the correct template."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_view_redirects_when_not_authenticated(self):
        """Test profile view redirects unauthenticated users to login."""
        from django.urls import reverse
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_profile_view_requires_login(self):
        """Test profile view requires authentication."""
        from django.urls import reverse
        response = self.client.get(reverse('profile'))
        # Should redirect to login page
        self.assertRedirects(
            response,
            f'/login/?next={reverse("profile")}',
            fetch_redirect_response=False
        )

    def test_profile_view_get_shows_current_user_data(self):
        """Test GET request displays profile form with current user data."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))

        # Check response contains form
        self.assertIn('form', response.context)

        # Check form has initial values from user profile
        form = response.context['form']
        self.assertEqual(form.initial['display_name'], 'Original Name')
        self.assertEqual(
            form.initial['monthly_budget'],
            Decimal('3000000.00')
        )

    def test_profile_view_get_contains_user_info(self):
        """Test GET request context contains user information."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))

        # Check user is in context
        self.assertEqual(response.context['user'], self.user)

    def test_profile_view_post_updates_display_name(self):
        """Test POST request with valid data updates user display_name."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'Updated Name',
            'monthly_budget': '3000000.00'
        }

        response = self.client.post(reverse('profile'), data)

        # Refresh profile from database
        self.profile.refresh_from_db()

        # Check display_name was updated
        self.assertEqual(self.profile.display_name, 'Updated Name')

    def test_profile_view_post_updates_monthly_budget(self):
        """Test POST request with valid data updates monthly_budget."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'Original Name',
            'monthly_budget': '5000000.00'
        }

        response = self.client.post(reverse('profile'), data)

        # Refresh profile from database
        self.profile.refresh_from_db()

        # Check monthly_budget was updated
        self.assertEqual(self.profile.monthly_budget, Decimal('5000000.00'))

    def test_profile_view_post_updates_both_fields(self):
        """Test POST request updates both display_name and monthly_budget."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'Brand New Name',
            'monthly_budget': '10000000.50'
        }

        response = self.client.post(reverse('profile'), data)

        # Refresh profile from database
        self.profile.refresh_from_db()

        # Check both fields were updated
        self.assertEqual(self.profile.display_name, 'Brand New Name')
        self.assertEqual(
            self.profile.monthly_budget,
            Decimal('10000000.50')
        )

    def test_profile_view_post_with_valid_data_redirects(self):
        """Test POST request with valid data redirects to profile page."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'New Name',
            'monthly_budget': '4000000.00'
        }

        response = self.client.post(reverse('profile'), data)

        # Should redirect to profile page
        self.assertRedirects(response, reverse('profile'))

    def test_profile_view_post_with_invalid_budget_shows_errors(self):
        """Test POST request with invalid monthly_budget shows errors."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'Test Name',
            'monthly_budget': 'invalid_amount'  # Invalid decimal
        }

        response = self.client.post(reverse('profile'), data)

        # Should not redirect (stays on same page)
        self.assertEqual(response.status_code, 200)

        # Should contain form errors
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_profile_view_post_with_negative_budget_shows_errors(self):
        """Test POST request with negative budget shows validation error."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'Test Name',
            'monthly_budget': '-1000.00'  # Negative value
        }

        response = self.client.post(reverse('profile'), data)

        # Should show form with errors
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_profile_view_post_with_display_name_too_long(self):
        """Test POST with display_name exceeding max_length shows error."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'a' * 101,  # Exceeds max_length of 100
            'monthly_budget': '3000000.00'
        }

        response = self.client.post(reverse('profile'), data)

        # Should show form with errors
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_profile_view_post_with_blank_display_name(self):
        """Test POST with blank display_name is allowed."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': '',  # Blank is allowed
            'monthly_budget': '3000000.00'
        }

        response = self.client.post(reverse('profile'), data)

        # Should succeed
        self.assertRedirects(response, reverse('profile'))

        # Refresh profile from database
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.display_name, '')

    def test_profile_view_post_with_blank_budget(self):
        """Test POST with blank monthly_budget is allowed (null)."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'Test Name',
            'monthly_budget': ''  # Blank/null is allowed
        }

        response = self.client.post(reverse('profile'), data)

        # Should succeed
        self.assertRedirects(response, reverse('profile'))

        # Refresh profile from database
        self.profile.refresh_from_db()
        self.assertIsNone(self.profile.monthly_budget)

    def test_profile_view_shows_success_message_after_update(self):
        """Test profile view shows success message after successful update."""
        from django.urls import reverse
        from django.contrib.messages import get_messages

        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'New Name',
            'monthly_budget': '4000000.00'
        }

        response = self.client.post(reverse('profile'), data, follow=True)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('successfully' in str(m).lower() for m in messages)
            or any('thành công' in str(m).lower() for m in messages)
        )

    def test_profile_view_only_updates_current_user_profile(self):
        """Test profile view only updates the logged-in user's profile."""
        from django.urls import reverse

        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        other_profile = other_user.profile
        other_profile.display_name = 'Other User'
        other_profile.save()

        # Login as first user
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'Updated Name',
            'monthly_budget': '5000000.00'
        }

        response = self.client.post(reverse('profile'), data)

        # Check first user's profile was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.display_name, 'Updated Name')

        # Check other user's profile was NOT updated
        other_profile.refresh_from_db()
        self.assertEqual(other_profile.display_name, 'Other User')

    def test_profile_view_get_method_allowed(self):
        """Test profile view accepts GET requests."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_post_method_allowed(self):
        """Test profile view accepts POST requests."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')

        data = {
            'display_name': 'Test',
            'monthly_budget': '1000000.00'
        }

        response = self.client.post(reverse('profile'), data)
        # Should redirect or return 200
        self.assertIn(response.status_code, [200, 302])

    def test_profile_view_context_has_user_profile(self):
        """Test profile view context contains user's profile object."""
        from django.urls import reverse
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))

        # Check profile or object is in context
        self.assertTrue(
            'profile' in response.context or 'object' in response.context
        )
