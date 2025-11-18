"""
Test suite for project directory structure verification.

This module contains tests to verify that templates and static
directories are properly created with correct structure.
"""

import os
from django.test import TestCase
from django.conf import settings


class TemplateDirectoryStructureTest(TestCase):
    """Test suite for verifying templates directory structure."""

    def test_main_templates_directory_exists(self):
        """Test that main templates directory exists in project root."""
        templates_path = os.path.join(settings.BASE_DIR, 'templates')
        self.assertTrue(
            os.path.exists(templates_path),
            f"Main templates directory should exist at {templates_path}"
        )
        self.assertTrue(
            os.path.isdir(templates_path),
            "templates path should be a directory"
        )

    def test_accounts_templates_subdirectory_exists(self):
        """Test that accounts subdirectory exists in templates."""
        accounts_templates_path = os.path.join(
            settings.BASE_DIR,
            'templates',
            'accounts'
        )
        self.assertTrue(
            os.path.exists(accounts_templates_path),
            "accounts subdirectory should exist in templates"
        )
        self.assertTrue(
            os.path.isdir(accounts_templates_path),
            "templates/accounts should be a directory"
        )

    def test_transactions_templates_subdirectory_exists(self):
        """Test that transactions subdirectory exists in templates."""
        transactions_templates_path = os.path.join(
            settings.BASE_DIR,
            'templates',
            'transactions'
        )
        self.assertTrue(
            os.path.exists(transactions_templates_path),
            "transactions subdirectory should exist in templates"
        )
        self.assertTrue(
            os.path.isdir(transactions_templates_path),
            "templates/transactions should be a directory"
        )

    def test_reports_templates_subdirectory_exists(self):
        """Test that reports subdirectory exists in templates."""
        reports_templates_path = os.path.join(
            settings.BASE_DIR,
            'templates',
            'reports'
        )
        self.assertTrue(
            os.path.exists(reports_templates_path),
            "reports subdirectory should exist in templates"
        )
        self.assertTrue(
            os.path.isdir(reports_templates_path),
            "templates/reports should be a directory"
        )


class StaticDirectoryStructureTest(TestCase):
    """Test suite for verifying static directory structure."""

    def test_main_static_directory_exists(self):
        """Test that main static directory exists in project root."""
        static_path = os.path.join(settings.BASE_DIR, 'static')
        self.assertTrue(
            os.path.exists(static_path),
            f"Main static directory should exist at {static_path}"
        )
        self.assertTrue(
            os.path.isdir(static_path),
            "static path should be a directory"
        )

    def test_css_subdirectory_exists(self):
        """Test that css subdirectory exists in static."""
        css_path = os.path.join(settings.BASE_DIR, 'static', 'css')
        self.assertTrue(
            os.path.exists(css_path),
            "css subdirectory should exist in static"
        )
        self.assertTrue(
            os.path.isdir(css_path),
            "static/css should be a directory"
        )

    def test_js_subdirectory_exists(self):
        """Test that js subdirectory exists in static."""
        js_path = os.path.join(settings.BASE_DIR, 'static', 'js')
        self.assertTrue(
            os.path.exists(js_path),
            "js subdirectory should exist in static"
        )
        self.assertTrue(
            os.path.isdir(js_path),
            "static/js should be a directory"
        )

    def test_images_subdirectory_exists(self):
        """Test that images subdirectory exists in static."""
        images_path = os.path.join(settings.BASE_DIR, 'static', 'images')
        self.assertTrue(
            os.path.exists(images_path),
            "images subdirectory should exist in static"
        )
        self.assertTrue(
            os.path.isdir(images_path),
            "static/images should be a directory"
        )


class DirectoryPermissionsTest(TestCase):
    """Test suite for verifying directory permissions."""

    def test_templates_directory_is_writable(self):
        """Test that templates directory has write permissions."""
        templates_path = os.path.join(settings.BASE_DIR, 'templates')
        self.assertTrue(
            os.access(templates_path, os.W_OK),
            "templates directory should be writable"
        )

    def test_static_directory_is_writable(self):
        """Test that static directory has write permissions."""
        static_path = os.path.join(settings.BASE_DIR, 'static')
        self.assertTrue(
            os.access(static_path, os.W_OK),
            "static directory should be writable"
        )
