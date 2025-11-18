"""
Views for the transactions app.

This module contains views for creating, updating, and deleting transactions.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from typing import Any
from datetime import datetime
from .models import Transaction, Category
from .forms import TransactionForm


class TransactionListView(LoginRequiredMixin, ListView):
    """
    Display list of transactions for authenticated users.

    Provides pagination (20 items per page) and filtering by:
    - date_from: Start date for date range filter
    - date_to: End date for date range filter
    - category: Filter by specific category ID
    - type: Filter by transaction type (income/expense)

    Only displays transactions owned by the current user.
    """

    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transaction_list'
    paginate_by = 20

    def get_queryset(self):
        """
        Filter queryset to current user's transactions with optional filters.

        Optimized with select_related to reduce database queries.

        Returns:
            QuerySet: Filtered transactions ordered by date (newest first)
        """
        queryset = Transaction.objects.filter(
            user=self.request.user
        ).select_related('category', 'user')

        # Filter by date range
        date_from = self.request.GET.get('date_from')
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=date_from_obj)
            except ValueError:
                pass  # Ignore invalid date format

        date_to = self.request.GET.get('date_to')
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=date_to_obj)
            except ValueError:
                pass  # Ignore invalid date format

        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            try:
                queryset = queryset.filter(category_id=int(category_id))
            except (ValueError, TypeError):
                pass  # Ignore invalid category ID

        # Filter by type
        transaction_type = self.request.GET.get('type')
        if transaction_type in ['income', 'expense']:
            queryset = queryset.filter(type=transaction_type)

        return queryset.order_by('-date', '-created_at')

    def get_context_data(self, **kwargs):
        """
        Add categories and filter parameters to context.

        Returns:
            dict: Context data with categories and current filters
        """
        context = super().get_context_data(**kwargs)

        # Add all categories for filter dropdown
        context['categories'] = Category.objects.all().order_by('type', 'name')

        # Add current filter values to context for form persistence
        context['current_date_from'] = self.request.GET.get('date_from', '')
        context['current_date_to'] = self.request.GET.get('date_to', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_type'] = self.request.GET.get('type', '')

        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    """
    Handle creation of new transactions.

    Requires user to be authenticated. Automatically sets the user
    from the request.
    """

    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:transaction_list')

    def get_form_kwargs(self):
        """Pass user to form for transaction creation."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Set user from request before saving."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Handle updating existing transactions.

    Requires user to be authenticated and only allows the owner
    to update their own transactions.
    """

    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:transaction_list')

    def get_form_kwargs(self):
        """Pass user to form for transaction update."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        """Check if user owns the transaction before processing request."""
        # Get transaction without filtering by user first to check ownership
        try:
            transaction = Transaction.objects.select_related(
                'category', 'user'
            ).get(pk=self.kwargs.get('pk'))
            if transaction.user != request.user:
                raise PermissionDenied(
                    "You don't have permission to edit this transaction."
                )
        except Transaction.DoesNotExist:
            pass  # Let get_object() handle 404

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filter queryset to only include current user's transactions.

        Optimized with select_related for category.
        """
        return Transaction.objects.filter(
            user=self.request.user
        ).select_related('category')


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handle deletion of transactions.

    Requires user to be authenticated and only allows the owner
    to delete their own transactions.
    """

    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transactions:transaction_list')

    def dispatch(self, request, *args, **kwargs):
        """Check if user owns the transaction before processing request."""
        # Get transaction without filtering by user first to check ownership
        try:
            transaction = Transaction.objects.select_related(
                'category', 'user'
            ).get(pk=self.kwargs.get('pk'))
            if transaction.user != request.user:
                raise PermissionDenied(
                    "You don't have permission to delete this transaction."
                )
        except Transaction.DoesNotExist:
            pass  # Let get_object() handle 404

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filter queryset to only include current user's transactions.

        Optimized with select_related for category.
        """
        return Transaction.objects.filter(
            user=self.request.user
        ).select_related('category')
