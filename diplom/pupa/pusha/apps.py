from django.apps import AppConfig

"""
Конфигурация приложения `pusha`.

Этот файл определяет конфигурацию для приложения `pusha`, включая
имя приложения и настройки для автоинкрементных полей.
"""

class PushaConfig(AppConfig):
    """
    Конфигурация приложения `pusha`.

    Атрибуты:
        default_auto_field: Поле по умолчанию для автоматического создания ID.
        name: Имя приложения, используемое в настройках проекта.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pusha'