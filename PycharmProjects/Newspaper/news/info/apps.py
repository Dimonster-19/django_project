from django.apps import AppConfig

class InfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'info'

    def ready(self):
        if not hasattr(self, 'signals_registered'):
            import info.signals
            self.signals_registered = True
