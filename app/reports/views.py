"""
Views for the reports app.

This module contains views for displaying financial reports and analytics.
"""

from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.http import JsonResponse
from datetime import date, timedelta, datetime
from typing import Any, Dict, Tuple, List
from decimal import Decimal
from transactions.models import Transaction, Category
from collections import defaultdict


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Display dashboard with current month statistics.

    Provides:
    - Total income for current month
    - Total expense for current month
    - Balance (income - expense)
    - Recent transactions (5-10 most recent)

    Only displays data for the authenticated user.
    Requires user to be logged in (@login_required).
    """

    template_name = 'reports/dashboard.html'
    login_url = '/accounts/login/'

    def get_current_month_range(self) -> Tuple[date, date]:
        """
        Get date range for current month.

        Returns:
            Tuple[date, date]: First day and last day of current month
        """
        today = date.today()
        start = today.replace(day=1)

        # Calculate last day of current month
        if today.month == 12:
            end = today.replace(month=12, day=31)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
            end = next_month - timedelta(days=1)

        return start, end

    def get_statistics(
        self, date_from: date, date_to: date
    ) -> Dict[str, Decimal]:
        """
        Calculate income and expense statistics for date range.

        Optimized to use single query with conditional aggregation.

        Args:
            date_from: Start date for filtering
            date_to: End date for filtering

        Returns:
            Dict with total_income, total_expense, and balance
        """
        from django.db.models import Sum, Q

        # Single query with conditional aggregation
        stats = Transaction.objects.filter(
            user=self.request.user,
            date__gte=date_from,
            date__lte=date_to
        ).aggregate(
            total_income=Sum('amount', filter=Q(type='income')),
            total_expense=Sum('amount', filter=Q(type='expense'))
        )

        income_sum = stats['total_income'] or Decimal('0')
        expense_sum = stats['total_expense'] or Decimal('0')
        balance = income_sum - expense_sum

        return {
            'total_income': income_sum,
            'total_expense': expense_sum,
            'balance': balance
        }

    def get_recent_transactions(self, limit: int = 10) -> List[Transaction]:
        """
        Get recent transactions for the user.

        Args:
            limit: Maximum number of transactions to return (default 10)

        Returns:
            QuerySet of recent Transaction objects, ordered by date desc
        """
        return Transaction.objects.filter(
            user=self.request.user
        ).select_related(
            'category'
        ).order_by('-date', '-created_at')[:limit]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Add dashboard statistics to context.

        Returns:
            dict: Context data with current month statistics and recent
                  transactions
        """
        context = super().get_context_data(**kwargs)

        # Get current month date range
        date_from, date_to = self.get_current_month_range()

        # Get statistics for current month
        statistics = self.get_statistics(date_from, date_to)
        context['total_income'] = statistics['total_income']
        context['total_expense'] = statistics['total_expense']
        context['balance'] = statistics['balance']

        # Get recent transactions (up to 10)
        context['recent_transactions'] = self.get_recent_transactions(10)

        # Add current month information for display
        today = date.today()
        context['current_month'] = today.month
        context['current_year'] = today.year

        return context


class ReportsView(LoginRequiredMixin, TemplateView):
    """
    Display financial reports with time range filtering.

    Provides statistics for:
    - Total income and expense for selected period
    - Balance calculation
    - Breakdown by category (both income and expense)

    Supports time range filtering:
    - today: Today's transactions
    - this_week: Current week (Monday to Sunday)
    - this_month: Current month
    - this_year: Current year
    - custom: Custom date range (requires date_from and date_to parameters)

    Only displays data for the authenticated user.
    """

    template_name = 'reports/reports.html'

    TIME_RANGE_CHOICES = [
        ('today', 'Hôm nay'),
        ('this_week', 'Tuần này'),
        ('this_month', 'Tháng này'),
        ('this_year', 'Năm này'),
        ('custom', 'Tùy chỉnh'),
    ]

    def get_date_range(self) -> Tuple[date, date]:
        """
        Calculate date range based on query parameters.

        Returns:
            Tuple[date, date]: Start date and end date for filtering
        """
        range_type = self.request.GET.get('range', 'this_month')
        today = date.today()

        if range_type == 'today':
            return today, today

        elif range_type == 'this_week':
            # Monday to Sunday
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            return start, end

        elif range_type == 'this_month':
            start = today.replace(day=1)
            # Last day of current month
            if today.month == 12:
                end = today.replace(month=12, day=31)
            else:
                next_month = today.replace(
                    month=today.month + 1, day=1
                )
                end = next_month - timedelta(days=1)
            return start, end

        elif range_type == 'this_year':
            start = today.replace(month=1, day=1)
            end = today.replace(month=12, day=31)
            return start, end

        elif range_type == 'custom':
            date_from_str = self.request.GET.get('date_from')
            date_to_str = self.request.GET.get('date_to')

            try:
                from datetime import datetime
                date_from = datetime.strptime(
                    date_from_str, '%Y-%m-%d'
                ).date() if date_from_str else today
                date_to = datetime.strptime(
                    date_to_str, '%Y-%m-%d'
                ).date() if date_to_str else today
                return date_from, date_to
            except (ValueError, TypeError):
                # Invalid date format, fallback to this_month
                return self._get_this_month_range(today)

        # Default to this_month for invalid range types
        return self._get_this_month_range(today)

    def _get_this_month_range(self, today: date) -> Tuple[date, date]:
        """Helper method to get this month's date range."""
        start = today.replace(day=1)
        if today.month == 12:
            end = today.replace(month=12, day=31)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
            end = next_month - timedelta(days=1)
        return start, end

    def get_current_range(self) -> str:
        """
        Get the current selected time range.

        Returns:
            str: Current range type, defaults to 'this_month'
        """
        range_type = self.request.GET.get('range', 'this_month')
        valid_ranges = [r[0] for r in self.TIME_RANGE_CHOICES]

        if range_type not in valid_ranges:
            return 'this_month'

        return range_type

    def get_statistics(
        self, date_from: date, date_to: date
    ) -> Dict[str, Decimal]:
        """
        Calculate income and expense statistics for date range.

        Optimized to use single query with conditional aggregation.

        Args:
            date_from: Start date for filtering
            date_to: End date for filtering

        Returns:
            Dict with total_income, total_expense, and balance
        """
        # Single query with conditional aggregation
        stats = Transaction.objects.filter(
            user=self.request.user,
            date__gte=date_from,
            date__lte=date_to
        ).aggregate(
            total_income=Sum('amount', filter=Q(type='income')),
            total_expense=Sum('amount', filter=Q(type='expense'))
        )

        income_sum = stats['total_income'] or Decimal('0.00')
        expense_sum = stats['total_expense'] or Decimal('0.00')
        balance = income_sum - expense_sum

        return {
            'total_income': income_sum,
            'total_expense': expense_sum,
            'balance': balance
        }

    def get_category_breakdown(
        self, date_from: date, date_to: date, transaction_type: str
    ):
        """
        Get breakdown of transactions by category.

        Args:
            date_from: Start date for filtering
            date_to: End date for filtering
            transaction_type: 'income' or 'expense'

        Returns:
            QuerySet with category breakdown (category__name, total)
        """
        return Transaction.objects.filter(
            user=self.request.user,
            date__gte=date_from,
            date__lte=date_to,
            type=transaction_type
        ).values(
            'category__name',
            'category__icon',
            'category__color'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Add report data to context.

        Returns:
            dict: Context data with statistics and filter options
        """
        context = super().get_context_data(**kwargs)

        # Add time range choices
        context['time_ranges'] = self.TIME_RANGE_CHOICES

        # Get current selected range
        current_range = self.get_current_range()
        context['current_range'] = current_range

        # Get date range
        date_from, date_to = self.get_date_range()
        context['date_from'] = date_from
        context['date_to'] = date_to

        # Get statistics
        statistics = self.get_statistics(date_from, date_to)
        context['total_income'] = statistics['total_income']
        context['total_expense'] = statistics['total_expense']
        context['balance'] = statistics['balance']

        # Get transaction count
        context['transaction_count'] = Transaction.objects.filter(
            user=self.request.user,
            date__gte=date_from,
            date__lte=date_to
        ).count()

        # Get category breakdowns
        context['income_by_category'] = self.get_category_breakdown(
            date_from, date_to, 'income'
        )
        context['expense_by_category'] = self.get_category_breakdown(
            date_from, date_to, 'expense'
        )

        # Add all categories for reference
        context['categories'] = Category.objects.all().order_by(
            'type', 'name'
        )

        # Add custom date values for form persistence
        context['custom_date_from'] = self.request.GET.get('date_from', '')
        context['custom_date_to'] = self.request.GET.get('date_to', '')

        return context


class ChartDataAPIView(LoginRequiredMixin, View):
    """
    API endpoint for chart data in JSON format.

    Supports multiple chart types:
    - bar_chart: Income/expense by time period (day/week/month)
    - pie_chart: Expense breakdown by category
    - line_chart: Monthly trend over time

    Returns data in Chart.js compatible format.
    """

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle GET request and return JSON chart data.

        Query parameters:
        - chart_type: Type of chart (bar_chart, pie_chart, line_chart)
        - period: Time grouping for bar chart (day, week, month)
        - months: Number of months for line chart (default 6)
        - date_from: Start date for filtering (YYYY-MM-DD)
        - date_to: End date for filtering (YYYY-MM-DD)

        Returns:
            JsonResponse: Chart data in Chart.js format
        """
        chart_type = request.GET.get('chart_type', 'bar_chart')

        if chart_type == 'pie_chart':
            return self.get_pie_chart_data()
        elif chart_type == 'line_chart':
            return self.get_line_chart_data()
        else:  # Default to bar_chart
            return self.get_bar_chart_data()

    def get_date_range(self) -> Tuple[date, date]:
        """
        Get date range from query parameters or use defaults.

        Returns:
            Tuple[date, date]: Start and end dates
        """
        date_from_str = self.request.GET.get('date_from')
        date_to_str = self.request.GET.get('date_to')
        today = date.today()

        try:
            if date_from_str and date_to_str:
                date_from = datetime.strptime(
                    date_from_str, '%Y-%m-%d'
                ).date()
                date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
                return date_from, date_to
        except (ValueError, TypeError):
            pass

        # Default to current month
        start = today.replace(day=1)
        if today.month == 12:
            end = today.replace(month=12, day=31)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
            end = next_month - timedelta(days=1)

        return start, end

    def get_bar_chart_data(self) -> JsonResponse:
        """
        Generate bar chart data for income/expense by time period.

        Optimized with values() and annotate() for efficient aggregation.

        Returns:
            JsonResponse: Bar chart data with labels and datasets
        """
        period = self.request.GET.get('period', 'month')
        date_from, date_to = self.get_date_range()

        # Get transactions for the user (no select_related needed for aggregation)
        transactions = Transaction.objects.filter(
            user=self.request.user,
            date__gte=date_from,
            date__lte=date_to
        )

        # Group by period
        if period == 'day':
            grouped = transactions.annotate(
                period_date=TruncDate('date')
            ).values('period_date', 'type').annotate(
                total=Sum('amount')
            ).order_by('period_date')
        elif period == 'week':
            grouped = transactions.annotate(
                period_date=TruncWeek('date')
            ).values('period_date', 'type').annotate(
                total=Sum('amount')
            ).order_by('period_date')
        else:  # month
            grouped = transactions.annotate(
                period_date=TruncMonth('date')
            ).values('period_date', 'type').annotate(
                total=Sum('amount')
            ).order_by('period_date')

        # Organize data
        labels = []
        income_data = {}
        expense_data = {}

        for item in grouped:
            period_key = item['period_date'].strftime('%Y-%m-%d')
            if period_key not in labels:
                labels.append(period_key)

            if item['type'] == 'income':
                income_data[period_key] = float(item['total'])
            else:
                expense_data[period_key] = float(item['total'])

        # Sort labels
        labels.sort()

        # Build datasets
        income_values = [income_data.get(label, 0) for label in labels]
        expense_values = [expense_data.get(label, 0) for label in labels]

        # Format labels for display
        formatted_labels = []
        for label in labels:
            dt = datetime.strptime(label, '%Y-%m-%d').date()
            if period == 'day':
                formatted_labels.append(dt.strftime('%d/%m'))
            elif period == 'week':
                formatted_labels.append(f"W{dt.isocalendar()[1]}")
            else:  # month
                formatted_labels.append(dt.strftime('%m/%Y'))

        data = {
            'labels': formatted_labels,
            'datasets': [
                {
                    'label': 'Thu nhập',
                    'data': income_values,
                    'backgroundColor': 'rgba(34, 197, 94, 0.7)',
                    'borderColor': 'rgba(34, 197, 94, 1)',
                    'borderWidth': 1
                },
                {
                    'label': 'Chi tiêu',
                    'data': expense_values,
                    'backgroundColor': 'rgba(239, 68, 68, 0.7)',
                    'borderColor': 'rgba(239, 68, 68, 1)',
                    'borderWidth': 1
                }
            ]
        }

        return JsonResponse(data)

    def get_pie_chart_data(self) -> JsonResponse:
        """
        Generate pie chart data for expense breakdown by category.

        Optimized using values() and annotate() for aggregation.

        Returns:
            JsonResponse: Pie chart data with category labels and values
        """
        date_from, date_to = self.get_date_range()

        # Get expense breakdown by category (values + annotate is efficient)
        expenses = Transaction.objects.filter(
            user=self.request.user,
            type='expense',
            date__gte=date_from,
            date__lte=date_to
        ).values(
            'category__name', 'category__color'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')

        labels = []
        values = []
        colors = []

        for expense in expenses:
            labels.append(expense['category__name'])
            values.append(float(expense['total']))
            colors.append(expense['category__color'])

        data = {
            'labels': labels,
            'datasets': [{
                'data': values,
                'backgroundColor': colors,
                'borderWidth': 1
            }]
        }

        return JsonResponse(data)

    def get_line_chart_data(self) -> JsonResponse:
        """
        Generate line chart data for monthly income/expense trend.

        Optimized using database-level aggregation with annotate().

        Returns:
            JsonResponse: Line chart data with monthly trends
        """
        months_count = int(self.request.GET.get('months', 6))
        today = date.today()

        # Calculate date range for the past N months
        start_date = today.replace(day=1) - timedelta(
            days=30 * (months_count - 1)
        )
        start_date = start_date.replace(day=1)

        # Get transactions grouped by month (efficient aggregation)
        transactions = Transaction.objects.filter(
            user=self.request.user,
            date__gte=start_date,
            date__lte=today
        ).annotate(
            month=TruncMonth('date')
        ).values('month', 'type').annotate(
            total=Sum('amount')
        ).order_by('month')

        # Organize data
        labels = []
        income_data = {}
        expense_data = {}

        for item in transactions:
            month_key = item['month'].strftime('%Y-%m')
            if month_key not in labels:
                labels.append(month_key)

            if item['type'] == 'income':
                income_data[month_key] = float(item['total'])
            else:
                expense_data[month_key] = float(item['total'])

        # Sort labels
        labels.sort()

        # Format labels
        formatted_labels = []
        for label in labels:
            dt = datetime.strptime(label + '-01', '%Y-%m-%d').date()
            formatted_labels.append(dt.strftime('%m/%Y'))

        # Build datasets
        income_values = [income_data.get(label, 0) for label in labels]
        expense_values = [expense_data.get(label, 0) for label in labels]

        data = {
            'labels': formatted_labels,
            'datasets': [
                {
                    'label': 'Thu nhập',
                    'data': income_values,
                    'borderColor': 'rgba(34, 197, 94, 1)',
                    'backgroundColor': 'rgba(34, 197, 94, 0.2)',
                    'fill': True,
                    'tension': 0.3
                },
                {
                    'label': 'Chi tiêu',
                    'data': expense_values,
                    'borderColor': 'rgba(239, 68, 68, 1)',
                    'backgroundColor': 'rgba(239, 68, 68, 0.2)',
                    'fill': True,
                    'tension': 0.3
                }
            ]
        }

        return JsonResponse(data)
