"""
ASGI config for pupa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

"""
Настройка ASGI для проекта Django.

1. Устанавливает переменную окружения `DJANGO_SETTINGS_MODULE`,
   указывающую на файл настроек проекта Django.
2. Создаёт экземпляр ASGI-приложения для обработки запросов.
"""

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pupa.settings')

# Создаём и экспортируем экземпляр ASGI-приложения
application = get_asgi_application()