#!/usr/bin/env python
"""Seed sample transactions for testing."""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from transactions.models import Category, Transaction

# Get or create test user
user, created = User.objects.get_or_create(
    username='toanpv',
    defaults={
        'email': 'toanpv@example.com',
        'first_name': 'Toan',
        'last_name': 'Pham'
    }
)
if created:
    user.set_password('admin123')
    user.save()
    print(f'Created user: {user.username}')
else:
    print(f'Using existing user: {user.username}')

# Get categories
food_cat = Category.objects.filter(name='Ăn uống', transaction_type='expense').first()
salary_cat = Category.objects.filter(name='Lương', transaction_type='income').first()
shopping_cat = Category.objects.filter(name='Mua sắm', transaction_type='expense').first()
transport_cat = Category.objects.filter(name='Di chuyển & Xăng xe', transaction_type='expense').first()

if not all([food_cat, salary_cat, shopping_cat, transport_cat]):
    print('ERROR: Required categories not found!')
    sys.exit(1)

# Create sample transactions
today = datetime.now().date()
transactions_data = [
    # This month - November 2025
    {'amount': 5000000, 'type': 'income', 'category': salary_cat, 'date': today.replace(day=1), 'note': 'Lương tháng 11'},
    {'amount': 100000, 'type': 'expense', 'category': food_cat, 'date': today, 'note': 'Ăn trưa'},
    {'amount': 50000, 'type': 'expense', 'category': transport_cat, 'date': today, 'note': 'Grab đi làm'},
    {'amount': 200000, 'type': 'expense', 'category': food_cat, 'date': today - timedelta(days=1), 'note': 'Đi ăn tối'},
    {'amount': 500000, 'type': 'expense', 'category': shopping_cat, 'date': today - timedelta(days=2), 'note': 'Mua quần áo'},
    
    # Last month - October 2025
    {'amount': 5000000, 'type': 'income', 'category': salary_cat, 'date': today.replace(month=10, day=1), 'note': 'Lương tháng 10'},
    {'amount': 150000, 'type': 'expense', 'category': food_cat, 'date': today.replace(month=10, day=15), 'note': 'Ăn trưa'},
    {'amount': 60000, 'type': 'expense', 'category': transport_cat, 'date': today.replace(month=10, day=20), 'note': 'Xăng xe'},
    {'amount': 300000, 'type': 'expense', 'category': shopping_cat, 'date': today.replace(month=10, day=25), 'note': 'Mua giày'},
    
    # September 2025
    {'amount': 4800000, 'type': 'income', 'category': salary_cat, 'date': today.replace(month=9, day=1), 'note': 'Lương tháng 9'},
    {'amount': 120000, 'type': 'expense', 'category': food_cat, 'date': today.replace(month=9, day=10), 'note': 'Ăn sáng'},
]

created_count = 0
for data in transactions_data:
    transaction, created = Transaction.objects.get_or_create(
        user=user,
        amount=data['amount'],
        transaction_type=data['type'],
        category=data['category'],
        date=data['date'],
        defaults={'note': data['note']}
    )
    if created:
        created_count += 1
        print(f'Created: {transaction}')

print(f'\nTotal transactions created: {created_count}')
print(f'Total transactions for {user.username}: {Transaction.objects.filter(user=user).count()}')
print('\nYou can now login with:')
print(f'Username: {user.username}')
print(f'Password: admin123')
