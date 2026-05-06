from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """Configuração da aplicação de autenticação."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'
    verbose_name = 'Autenticação'
