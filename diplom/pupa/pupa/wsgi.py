"""
WSGI config for pupa project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

"""
WSGI конфигурация для проекта `pupa`.

Этот файл предоставляет точку входа для WSGI-совместимых веб-серверов,
чтобы они могли взаимодействовать с вашим Django-приложением.

Подробнее: https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pupa.settings')

# Создаём WSGI-приложение
application = get_wsgi_application()