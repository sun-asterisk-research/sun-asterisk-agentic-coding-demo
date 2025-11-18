"""
Test suite for Django app setup verification.

This module contains tests to verify that all required Django apps
are properly created and configured in the project structure.
"""

import os
from django.test import TestCase
from django.conf import settings


class AppSetupTest(TestCase):
    """Test suite for verifying Django apps are created correctly."""

    def test_transactions_app_exists(self):
        """Test that transactions app directory exists in project."""
        app_path = os.path.join(settings.BASE_DIR, 'transactions')
        self.assertTrue(
            os.path.exists(app_path),
            f"Transactions app directory should exist at {app_path}"
        )

    def test_transactions_app_has_init(self):
        """Test that transactions app has __init__.py file."""
        init_path = os.path.join(
            settings.BASE_DIR,
            'transactions',
            '__init__.py'
        )
        self.assertTrue(
            os.path.exists(init_path),
            "Transactions app should have __init__.py file"
        )

    def test_transactions_app_has_apps_config(self):
        """Test that transactions app has apps.py configuration."""
        apps_path = os.path.join(settings.BASE_DIR, 'transactions', 'apps.py')
        self.assertTrue(
            os.path.exists(apps_path),
            "Transactions app should have apps.py file"
        )

    def test_transactions_app_has_models(self):
        """Test that transactions app has models.py file."""
        models_path = os.path.join(
            settings.BASE_DIR,
            'transactions',
            'models.py'
        )
        self.assertTrue(
            os.path.exists(models_path),
            "Transactions app should have models.py file"
        )

    def test_transactions_app_has_views(self):
        """Test that transactions app has views.py file."""
        views_path = os.path.join(
            settings.BASE_DIR,
            'transactions',
            'views.py'
        )
        self.assertTrue(
            os.path.exists(views_path),
            "Transactions app should have views.py file"
        )

    def test_transactions_app_has_tests(self):
        """Test that transactions app has tests.py file."""
        tests_path = os.path.join(
            settings.BASE_DIR,
            'transactions',
            'tests.py'
        )
        self.assertTrue(
            os.path.exists(tests_path),
            "Transactions app should have tests.py file"
        )

    def test_transactions_app_has_admin(self):
        """Test that transactions app has admin.py file."""
        admin_path = os.path.join(
            settings.BASE_DIR,
            'transactions',
            'admin.py'
        )
        self.assertTrue(
            os.path.exists(admin_path),
            "Transactions app should have admin.py file"
        )
