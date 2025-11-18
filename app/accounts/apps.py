"""Django app configuration for accounts app."""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for the accounts application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """
        Import signal handlers when the app is ready.

        This method is called when Django starts. It imports the signals
        module to register signal handlers.
        """
        import accounts.signals  # noqa: F401
