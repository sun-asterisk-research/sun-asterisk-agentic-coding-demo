"""Views for transactions app."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Transaction
from .forms import TransactionForm


@login_required
def dashboard(request):
    """Dashboard view with summary statistics."""
    from django.db.models import Sum, Count
    from decimal import Decimal
    
    # Get all user's transactions
    user_transactions = Transaction.objects.filter(user=request.user)
    
    # Calculate summary stats
    income_sum = user_transactions.filter(
        transaction_type='income'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    expense_sum = user_transactions.filter(
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    balance = income_sum - expense_sum
    
    # Get recent transactions (last 10)
    recent_transactions = user_transactions.select_related(
        'category'
    ).order_by('-date', '-created_at')[:10]
    
    # Get top 5 expense categories
    top_categories = user_transactions.filter(
        transaction_type='expense'
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')[:5]
    
    context = {
        'total_income': income_sum,
        'total_expense': expense_sum,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'top_categories': top_categories,
    }
    
    return render(request, 'transactions/dashboard.html', context)


@login_required
def transaction_list(request):
    """Transaction list view with pagination."""
    transactions = Transaction.objects.filter(
        user=request.user
    ).select_related('category')
    
    # Pagination
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'transactions': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'transactions/transaction_list.html', context)


@login_required
def transaction_create(request):
    """Transaction create view."""
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save()
            type_display = transaction.get_transaction_type_display()
            messages.success(
                request,
                f'Đã thêm {type_display} {transaction.amount:,} VNĐ'
            )
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'transactions/transaction_form.html', {
        'form': form
    })


@login_required
def transaction_update(request, pk):
    """Transaction update view."""
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user
    )
    
    if request.method == 'POST':
        form = TransactionForm(
            request.POST,
            instance=transaction,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật giao dịch')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    
    return render(request, 'transactions/transaction_form.html', {
        'form': form
    })


@login_required
def transaction_delete(request, pk):
    """Transaction delete view."""
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user
    )
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Đã xóa giao dịch')
        return redirect('transaction_list')
    
    return render(
        request,
        'transactions/transaction_confirm_delete.html',
        {'object': transaction}
    )


@login_required
def reports(request):
    """Reports view with charts and analytics."""
    from django.db.models import Sum, Count
    from django.db.models.functions import TruncMonth
    from datetime import datetime, timedelta
    from decimal import Decimal
    import json
    
    # Get date range from request or default to last 6 months
    end_date = request.GET.get('end_date')
    start_date = request.GET.get('start_date')
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        from django.utils import timezone
        end_date = timezone.now().date()
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = end_date - timedelta(days=180)  # 6 months
    
    # Get user's transactions in date range
    transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    # Monthly income vs expense
    monthly_data = transactions.annotate(
        month=TruncMonth('date')
    ).values('month', 'transaction_type').annotate(
        total=Sum('amount')
    ).order_by('month')
    
    # Convert to JSON-serializable format
    monthly_data_list = []
    for item in monthly_data:
        monthly_data_list.append({
            'month': item['month'].strftime('%Y-%m-%d'),
            'transaction_type': item['transaction_type'],
            'total': float(item['total'])
        })
    
    # Category breakdown
    category_data = transactions.filter(
        transaction_type='expense'
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')[:10]
    
    # Convert to JSON-serializable format
    category_data_list = []
    for item in category_data:
        category_data_list.append({
            'category__name': item['category__name'],
            'total': float(item['total'])
        })
    
    # Summary statistics
    total_income = transactions.filter(transaction_type='income').aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    
    total_expense = transactions.filter(transaction_type='expense').aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'monthly_data_json': json.dumps(monthly_data_list),
        'category_data': category_data_list,  # Keep as list for template loop
        'category_data_json': json.dumps(category_data_list),  # JSON for chart
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
    }
    
    return render(request, 'transactions/reports.html', context)
