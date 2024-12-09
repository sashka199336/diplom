"""
URL configuration for pupa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# pupa/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from pusha import views  # Предполагается, что ваше приложение называется "pusha"

"""
URL-конфигурация для проекта `pupa`.

Этот файл содержит маршруты для:
1. Административного интерфейса.
2. Аутентификации пользователей (логин, логаут, регистрация).
3. Основных представлений приложения `pusha`.
4. Обработки медиа-файлов в режиме разработки.

Каждый маршрут связывает URL с соответствующей функцией или классом представления.
"""

urlpatterns = [
    # Административный интерфейс Django
    path('admin/', admin.site.urls),

    # Домашняя страница
    path('', views.home_view, name='home'),

    # Регистрация пользователя
    path('register/', views.register_view, name='register'),

    # Панель управления для аутентифицированных пользователей
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Страница входа в систему
    path('login/', views.login_view, name='login'),

    # Страница выхода из системы
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Добавление изображений в ленту
    path('add_image_feed/', views.add_image_feed_view, name='add_image_feed'),

    # Страница логина для модуля object_detection (если отличается от основного логина)
    path('object_detection/login/', views.login_view, name='object_detection_login'),

    # Защищённая страница для object_detection
    path('object_detection/', views.object_detection_view, name='object_detection'),

    # Перенаправление на регистрацию
    path('redirect_to_register/', views.redirect_to_register, name='redirect_to_register'),

    # Альтернативный маршрут для выхода из системы, перенаправляющий на страницу регистрации
    path('logout/', LogoutView.as_view(next_page='register'), name='logout'),
]

# Обработка медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)