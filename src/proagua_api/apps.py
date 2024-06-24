from django.apps import AppConfig


class ProaguaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proagua_api'

    def ready(self):
        import proagua_api.signals
