# pusha/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from pusha import views  # Ваше приложение называется "pusha"
from django.contrib.auth.views import LogoutView

"""
URL-конфигурация для проекта.

Этот файл определяет маршруты для административной панели,
аутентификации, регистрации, работы с изображениями и других страниц.
"""

urlpatterns = [
    # Административный интерфейс Django
    path('admin/', admin.site.urls),

    # Домашняя страница
    path('', views.home_view, name='home'),

    # Регистрация пользователя
    path('register/', views.register_view, name='register'),

    # Панель управления (доступна только аутентифицированным пользователям)
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Страница логина
    path('login/', views.login_view, name='login'),

    # Страница выхода из системы
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Добавление изображений в ленту
    path('add_image_feed/', views.add_image_feed_view, name='add_image_feed'),

    # Страница логина для object_detection (если отличается от основной страницы логина)
    path('object_detection/login/', views.login_view, name='object_detection_login'),

    # Страница object_detection (защищена аутентификацией)
    path('object_detection/', views.object_detection_view, name='object_detection'),

    # Перенаправление на регистрацию (если требуется)
    path('redirect_to_register/', views.redirect_to_register, name='redirect_to_register'),

    # Альтернативный маршрут выхода с редиректом на страницу регистрации
    path('logout/', LogoutView.as_view(next_page='register'), name='logout'),
]