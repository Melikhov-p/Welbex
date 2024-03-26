from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    class Meta:
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'
