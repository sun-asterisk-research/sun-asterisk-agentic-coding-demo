"""
Test suite for template structure and content.

Tests verify that templates exist, contain required elements,
and follow Bootstrap 5 best practices.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
import os


class BaseTemplateTest(TestCase):
    """Test suite for base.html template."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'templates',
            'base.html'
        )

    def test_base_template_exists(self):
        """Test base.html template file exists."""
        self.assertTrue(
            os.path.exists(self.template_path),
            f"base.html template should exist at {self.template_path}"
        )

    def test_base_template_contains_bootstrap_css(self):
        """Test base.html includes Bootstrap 5 CSS CDN link."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            'bootstrap',
            content.lower(),
            "base.html should include Bootstrap CSS CDN"
        )
        self.assertIn(
            'css',
            content.lower(),
            "base.html should include CSS link"
        )

    def test_base_template_contains_bootstrap_js(self):
        """Test base.html includes Bootstrap 5 JS CDN link."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            'bootstrap',
            content.lower(),
            "base.html should include Bootstrap JS CDN"
        )
        self.assertIn(
            'bundle.min.js',
            content.lower(),
            "base.html should include Bootstrap bundle JS"
        )

    def test_base_template_has_title_block(self):
        """Test base.html contains title block."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            '{% block title %}',
            content,
            "base.html should have title block"
        )
        self.assertIn(
            '{% endblock title %}',
            content,
            "base.html should close title block"
        )

    def test_base_template_has_extra_css_block(self):
        """Test base.html contains extra_css block."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            '{% block extra_css %}',
            content,
            "base.html should have extra_css block"
        )
        self.assertIn(
            '{% endblock extra_css %}',
            content,
            "base.html should close extra_css block"
        )

    def test_base_template_has_content_block(self):
        """Test base.html contains content block."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            '{% block content %}',
            content,
            "base.html should have content block"
        )
        self.assertIn(
            '{% endblock content %}',
            content,
            "base.html should close content block"
        )

    def test_base_template_has_extra_js_block(self):
        """Test base.html contains extra_js block."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            '{% block extra_js %}',
            content,
            "base.html should have extra_js block"
        )
        self.assertIn(
            '{% endblock extra_js %}',
            content,
            "base.html should close extra_js block"
        )

    def test_base_template_has_navbar(self):
        """Test base.html contains navbar element."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            'navbar',
            content.lower(),
            "base.html should have navbar"
        )

    def test_navbar_contains_brand_name(self):
        """Test navbar contains 'Personal Finance Tracker' brand name."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            'Personal Finance Tracker',
            content,
            "Navbar should contain 'Personal Finance Tracker' brand name"
        )

    def test_navbar_has_responsive_toggle(self):
        """Test navbar has responsive collapse toggle for mobile."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            'navbar-toggler',
            content,
            "Navbar should have responsive toggle button"
        )
        self.assertIn(
            'data-bs-toggle="collapse"',
            content,
            "Navbar toggle should use Bootstrap 5 collapse"
        )

    def test_navbar_has_menu_links(self):
        """Test navbar contains main section links."""
        with open(self.template_path, 'r') as f:
            content = f.read()

        required_links = ['Dashboard', 'Transactions', 'Reports', 'Profile']
        for link_text in required_links:
            self.assertIn(
                link_text,
                content,
                f"Navbar should contain '{link_text}' link"
            )

    def test_navbar_has_user_dropdown(self):
        """Test navbar contains user menu dropdown."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            'dropdown',
            content.lower(),
            "Navbar should have dropdown menu for user"
        )

    def test_template_uses_green_color_scheme(self):
        """Test template uses green color (#22c55e) in styling."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            '#22c55e',
            content.lower(),
            "Template should use green color #22c55e"
        )

    def test_template_is_valid_html5(self):
        """Test template has valid HTML5 structure."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            '<!DOCTYPE html>',
            content,
            "Template should have HTML5 doctype"
        )
        self.assertIn(
            '<html',
            content,
            "Template should have html tag"
        )
        self.assertIn(
            '<head>',
            content,
            "Template should have head section"
        )
        self.assertIn(
            '<body>',
            content,
            "Template should have body section"
        )

    def test_template_has_viewport_meta(self):
        """Test template includes viewport meta tag for responsive design."""
        with open(self.template_path, 'r') as f:
            content = f.read()
        self.assertIn(
            'viewport',
            content.lower(),
            "Template should have viewport meta tag"
        )
        self.assertIn(
            'width=device-width',
            content.lower(),
            "Viewport should include width=device-width"
        )
