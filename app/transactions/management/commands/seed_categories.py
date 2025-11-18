"""
Management command to seed initial categories for the transactions app.

This command creates 17 predefined categories (11 expense + 6 income)
for users to categorize their financial transactions.
"""

from django.core.management.base import BaseCommand
from transactions.models import Category


class Command(BaseCommand):
    """
    Django management command to seed predefined categories.

    Creates 17 categories with Vietnamese names, icons, and colors:
    - 11 expense categories
    - 6 income categories

    The command is idempotent - running it multiple times won't create
    duplicates.
    """

    help = 'Seed 17 predefined categories (11 expense + 6 income)'

    def handle(self, *args, **options):
        """
        Execute the command to seed categories.

        Args:
            *args: Variable length argument list
            **options: Arbitrary keyword arguments

        Returns:
            None. Outputs success message to stdout.
        """
        # Define expense categories (11 categories)
        expense_categories = [
            {
                'name': 'Ăn uống',
                'icon': '🍔',
                'type': 'expense',
                'color': '#ef4444'
            },
            {
                'name': 'Xăng xe',
                'icon': '🚗',
                'type': 'expense',
                'color': '#f97316'
            },
            {
                'name': 'Nhà cửa',
                'icon': '🏠',
                'type': 'expense',
                'color': '#8b5cf6'
            },
            {
                'name': 'Mua sắm',
                'icon': '👕',
                'type': 'expense',
                'color': '#ec4899'
            },
            {
                'name': 'Y tế',
                'icon': '💊',
                'type': 'expense',
                'color': '#14b8a6'
            },
            {
                'name': 'Giáo dục',
                'icon': '📚',
                'type': 'expense',
                'color': '#3b82f6'
            },
            {
                'name': 'Giải trí',
                'icon': '🎬',
                'type': 'expense',
                'color': '#f59e0b'
            },
            {
                'name': 'Điện thoại/Internet',
                'icon': '📱',
                'type': 'expense',
                'color': '#06b6d4'
            },
            {
                'name': 'Gia đình',
                'icon': '👨‍👩‍👧',
                'type': 'expense',
                'color': '#84cc16'
            },
            {
                'name': 'Quà tặng',
                'icon': '🎁',
                'type': 'expense',
                'color': '#a855f7'
            },
            {
                'name': 'Khác',
                'icon': '⚡',
                'type': 'expense',
                'color': '#6b7280'
            },
        ]

        # Define income categories (6 categories)
        income_categories = [
            {
                'name': 'Lương',
                'icon': '💰',
                'type': 'income',
                'color': '#22c55e'
            },
            {
                'name': 'Thưởng',
                'icon': '💼',
                'type': 'income',
                'color': '#16a34a'
            },
            {
                'name': 'Đầu tư',
                'icon': '📈',
                'type': 'income',
                'color': '#15803d'
            },
            {
                'name': 'Thu nhập phụ',
                'icon': '🎯',
                'type': 'income',
                'color': '#059669'
            },
            {
                'name': 'Quà tặng',
                'icon': '🎁',
                'type': 'income',
                'color': '#10b981'
            },
            {
                'name': 'Khác',
                'icon': '⚡',
                'type': 'income',
                'color': '#14532d'
            },
        ]

        # Combine all categories
        all_categories = expense_categories + income_categories

        # Counter for created categories
        created_count = 0

        # Create categories if they don't exist
        for category_data in all_categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                type=category_data['type'],
                defaults={
                    'icon': category_data['icon'],
                    'color': category_data['color']
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {category.icon} {category.name} "
                        f"({category.get_type_display()})"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Already exists: {category.icon} {category.name} "
                        f"({category.get_type_display()})"
                    )
                )

        # Final summary
        total_categories = Category.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully seeded categories!"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created: {created_count} new categories"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Total: {total_categories} categories in database "
                f"(17 categories expected)"
            )
        )
