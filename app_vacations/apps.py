from django.apps import AppConfig


class AppVacationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_vacations'

    def ready(self):
        import app_vacations.signals
