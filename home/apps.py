from django.apps import AppConfig

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

def ready(self):
        import home.signals  # substitua pelo caminho do seu arquivo de signals