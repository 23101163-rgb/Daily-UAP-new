from django.apps import AppConfig

class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daily_uap.search'  # ✅ must match your package path
