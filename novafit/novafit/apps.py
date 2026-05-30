from django.apps import AppConfig


class NovafitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'novafit'
    verbose_name = 'NovaFit Gimnasio'

    def ready(self):
        pass
