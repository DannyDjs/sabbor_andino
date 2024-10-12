from django.apps import AppConfig


class TGastronomicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 't_gastronomico'
    
    def ready(self):
        import t_gastronomico.signals
