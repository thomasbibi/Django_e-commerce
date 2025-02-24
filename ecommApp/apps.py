from django.apps import AppConfig


class EcommappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommApp'

    def ready(self):
        import ecommApp.signals
