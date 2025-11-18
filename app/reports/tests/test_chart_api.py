# -*- coding: utf-8 -*-
"""
Tests for ChartDataAPIView.

This module contains tests for the chart data API endpoint.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from decimal import Decimal
from transactions.models import Transaction, Category
import json


class ChartDataAPIViewTest(TestCase):
    """Test suite for ChartDataAPIView API endpoint."""

    def setUp(self):
        """Set up test data for chart API tests."""
        self.client = Client()

        # Create test user
        self.user = User.objects.create_user(
            username='chartuser',
            email='chart@example.com',
            password='testpass123'
        )

        # Create another user for permission testing
        self.other_user = User.objects.create_user(
            username='otherchartuser',
            email='otherchart@example.com',
            password='testpass123'
        )

        # Create categories
        self.income_category = Category.objects.create(
            name='Salary',
            type='income',
            color='#22c55e'
        )

        self.expense_category1 = Category.objects.create(
            name='Food',
            type='expense',
            color='#ef4444'
        )

        self.expense_category2 = Category.objects.create(
            name='Transport',
            type='expense',
            color='#f59e0b'
        )

        # Create transactions for this month
        today = date.today()

        # Income transactions
        Transaction.objects.create(
            user=self.user,
            category=self.income_category,
            type='income',
            amount=Decimal('5000000'),
            date=today,
            note='Salary'
        )

        Transaction.objects.create(
            user=self.user,
            category=self.income_category,
            type='income',
            amount=Decimal('1000000'),
            date=today - timedelta(days=5),
            note='Bonus'
        )

        # Expense transactions
        Transaction.objects.create(
            user=self.user,
            category=self.expense_category1,
            type='expense',
            amount=Decimal('500000'),
            date=today,
            note='Lunch'
        )

        Transaction.objects.create(
            user=self.user,
            category=self.expense_category1,
            type='expense',
            amount=Decimal('300000'),
            date=today - timedelta(days=2),
            note='Dinner'
        )

        Transaction.objects.create(
            user=self.user,
            category=self.expense_category2,
            type='expense',
            amount=Decimal('200000'),
            date=today - timedelta(days=1),
            note='Taxi'
        )

        # Create transaction for other user (should not appear)
        Transaction.objects.create(
            user=self.other_user,
            category=self.income_category,
            type='income',
            amount=Decimal('10000000'),
            date=today,
            note='Other user income'
        )

    def test_api_requires_authentication(self):
        """Test API endpoint requires user to be logged in."""
        response = self.client.get(reverse('reports:chart-data'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_api_returns_json_response(self):
        """Test API returns JSON response with correct content type."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(reverse('reports:chart-data'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_api_bar_chart_data_structure(self):
        """Test bar chart returns correct data structure for Chart.js."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'bar_chart', 'period': 'week'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)
        self.assertIsInstance(data['labels'], list)
        self.assertIsInstance(data['datasets'], list)

        # Check datasets structure
        for dataset in data['datasets']:
            self.assertIn('label', dataset)
            self.assertIn('data', dataset)
            self.assertIn('backgroundColor', dataset)

    def test_api_pie_chart_data_structure(self):
        """Test pie chart returns correct data structure for categories."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'pie_chart'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)
        self.assertIsInstance(data['labels'], list)
        self.assertIsInstance(data['datasets'], list)

        # Pie chart should have category data
        if len(data['labels']) > 0:
            self.assertIn('backgroundColor', data['datasets'][0])

    def test_api_line_chart_data_structure(self):
        """Test line chart returns correct data structure for trends."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'line_chart'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)
        self.assertIsInstance(data['labels'], list)
        self.assertIsInstance(data['datasets'], list)

    def test_api_filters_by_user(self):
        """Test API only returns data for authenticated user."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'bar_chart', 'period': 'month'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        # Calculate total from response
        total_income = 0
        total_expense = 0
        for dataset in data['datasets']:
            label = dataset.get('label', '')
            # Check for income labels (Vietnamese: "Thu nhap" or English: "Income")
            if 'thu' in label.lower() and 'nh' in label.lower():
                total_income = sum(float(x) for x in dataset['data'])
            # Check for expense labels (Vietnamese: "Chi tieu" or English: "Expense")
            elif 'chi' in label.lower() and 't' in label.lower():
                total_expense = sum(float(x) for x in dataset['data'])

        # Should match chartuser's data only (not include other_user's 10,000,000)
        self.assertAlmostEqual(total_income, 6000000, delta=1)
        self.assertAlmostEqual(total_expense, 1000000, delta=1)

    def test_api_bar_chart_period_day(self):
        """Test bar chart with daily period grouping."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'bar_chart', 'period': 'day'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIsInstance(data['labels'], list)
        # Labels should be dates
        self.assertTrue(len(data['labels']) > 0)

    def test_api_bar_chart_period_week(self):
        """Test bar chart with weekly period grouping."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'bar_chart', 'period': 'week'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIsInstance(data['labels'], list)

    def test_api_bar_chart_period_month(self):
        """Test bar chart with monthly period grouping."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'bar_chart', 'period': 'month'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIsInstance(data['labels'], list)

    def test_api_pie_chart_expense_by_category(self):
        """Test pie chart shows expense breakdown by category."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'pie_chart'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        # Should have category names in labels
        if len(data['labels']) > 0:
            # Check that categories with expenses appear
            total_expenses = sum(data['datasets'][0]['data'])
            self.assertGreater(total_expenses, 0)

    def test_api_line_chart_monthly_trend(self):
        """Test line chart shows monthly income/expense trend."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'line_chart', 'months': '6'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIsInstance(data['labels'], list)
        self.assertIsInstance(data['datasets'], list)

    def test_api_date_range_filtering(self):
        """Test API supports date range filtering."""
        self.client.login(username='chartuser', password='testpass123')

        today = date.today()
        date_from = (today - timedelta(days=7)).strftime('%Y-%m-%d')
        date_to = today.strftime('%Y-%m-%d')

        response = self.client.get(
            reverse('reports:chart-data'),
            {
                'chart_type': 'bar_chart',
                'period': 'day',
                'date_from': date_from,
                'date_to': date_to
            }
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIsInstance(data, dict)

    def test_api_invalid_chart_type_defaults(self):
        """Test API handles invalid chart type gracefully."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'invalid_type'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        # Should return default chart or empty data
        self.assertIn('labels', data)
        self.assertIn('datasets', data)

    def test_api_default_chart_type(self):
        """Test API uses default chart type when not specified."""
        self.client.login(username='chartuser', password='testpass123')
        response = self.client.get(reverse('reports:chart-data'))
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)

    def test_api_empty_data_handling(self):
        """Test API handles users with no transactions."""
        # Create new user with no transactions
        new_user = User.objects.create_user(
            username='emptyuser',
            email='empty@example.com',
            password='testpass123'
        )

        self.client.login(username='emptyuser', password='testpass123')
        response = self.client.get(
            reverse('reports:chart-data'),
            {'chart_type': 'bar_chart'}
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)
