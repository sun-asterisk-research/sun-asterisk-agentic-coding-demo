"""
Tests for Django settings configuration.

This module tests that all required apps are properly registered
in INSTALLED_APPS and configured correctly.
"""

from django.test import TestCase
from django.conf import settings


class SettingsConfigTest(TestCase):
    """Test suite for settings configuration."""

    def test_accounts_app_is_installed(self):
        """Test that accounts app is registered in INSTALLED_APPS."""
        self.assertIn('accounts.apps.AccountsConfig', settings.INSTALLED_APPS)

    def test_transactions_app_is_installed(self):
        """Test that transactions app is registered in INSTALLED_APPS."""
        self.assertIn(
            'transactions.apps.TransactionsConfig',
            settings.INSTALLED_APPS
        )

    def test_reports_app_is_installed(self):
        """Test that reports app is registered in INSTALLED_APPS."""
        self.assertIn('reports.apps.ReportsConfig', settings.INSTALLED_APPS)

    def test_all_custom_apps_are_installed(self):
        """Test that all three custom apps are registered together."""
        custom_apps = [
            'accounts.apps.AccountsConfig',
            'transactions.apps.TransactionsConfig',
            'reports.apps.ReportsConfig',
        ]
        for app in custom_apps:
            with self.subTest(app=app):
                self.assertIn(app, settings.INSTALLED_APPS)

    def test_custom_apps_come_after_django_apps(self):
        """Test that custom apps are registered after Django built-in apps."""
        # Find indices of Django apps and custom apps
        admin_index = settings.INSTALLED_APPS.index(
            'django.contrib.admin'
        )

        # Custom apps should be registered
        if 'accounts.apps.AccountsConfig' in settings.INSTALLED_APPS:
            accounts_index = settings.INSTALLED_APPS.index(
                'accounts.apps.AccountsConfig'
            )
            self.assertGreater(
                accounts_index,
                admin_index,
                "Custom apps should come after Django built-in apps"
            )


class TimeZoneAndLanguageTest(TestCase):
    """Test suite for timezone and language configuration."""

    def test_timezone_is_asia_ho_chi_minh(self):
        """Test that timezone is set to Asia/Ho_Chi_Minh."""
        self.assertEqual(settings.TIME_ZONE, 'Asia/Ho_Chi_Minh')

    def test_language_code_is_vietnamese(self):
        """Test that language code is set to Vietnamese."""
        self.assertEqual(settings.LANGUAGE_CODE, 'vi')

    def test_use_i18n_is_enabled(self):
        """Test that internationalization is enabled."""
        self.assertTrue(settings.USE_I18N)

    def test_use_tz_is_enabled(self):
        """Test that timezone support is enabled."""
        self.assertTrue(settings.USE_TZ)


class StaticFilesConfigTest(TestCase):
    """Test suite for static files configuration."""

    def test_static_url_is_configured(self):
        """Test that STATIC_URL is configured."""
        # Django may normalize this to '/static/' so check both
        self.assertIn(settings.STATIC_URL, ['static/', '/static/'])

    def test_static_root_is_configured(self):
        """Test that STATIC_ROOT is configured."""
        self.assertIsNotNone(settings.STATIC_ROOT)
        self.assertTrue(str(settings.STATIC_ROOT).endswith('staticfiles'))

    def test_staticfiles_dirs_is_configured(self):
        """Test that STATICFILES_DIRS is configured."""
        self.assertIsNotNone(settings.STATICFILES_DIRS)
        self.assertGreater(len(settings.STATICFILES_DIRS), 0)
        # Check that it includes the static directory
        self.assertTrue(
            any(str(d).endswith('static') for d in settings.STATICFILES_DIRS)
        )


class MediaFilesConfigTest(TestCase):
    """Test suite for media files configuration."""

    def test_media_url_is_configured(self):
        """Test that MEDIA_URL is configured."""
        # Django may normalize this to '/media/' so check both
        self.assertIn(settings.MEDIA_URL, ['media/', '/media/'])

    def test_media_root_is_configured(self):
        """Test that MEDIA_ROOT is configured."""
        self.assertIsNotNone(settings.MEDIA_ROOT)
        self.assertTrue(str(settings.MEDIA_ROOT).endswith('media'))


class AuthenticationConfigTest(TestCase):
    """Test suite for authentication URL configuration."""

    def test_login_url_is_configured(self):
        """Test that LOGIN_URL is configured."""
        self.assertEqual(settings.LOGIN_URL, 'accounts:login')

    def test_login_redirect_url_is_configured(self):
        """Test that LOGIN_REDIRECT_URL is configured."""
        self.assertEqual(settings.LOGIN_REDIRECT_URL, 'reports:dashboard')

    def test_logout_redirect_url_is_configured(self):
        """Test that LOGOUT_REDIRECT_URL is configured."""
        self.assertEqual(settings.LOGOUT_REDIRECT_URL, 'accounts:login')
