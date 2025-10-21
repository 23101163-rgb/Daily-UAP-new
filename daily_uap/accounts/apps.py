from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daily_uap.accounts'

    def ready(self):
        import daily_uap.accounts.signals
