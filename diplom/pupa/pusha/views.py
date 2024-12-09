from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib import messages
from .forms import ImageUploadForm, UploadImageForm
from .models import ImageUpload
from .utils import recognize_image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import io

"""
Этот модуль содержит представления для приложения `pusha`.

Здесь реализованы:
1. Аутентификация пользователей (вход, регистрация, выход).
2. Отображение главной страницы, панели управления и других страниц.
3. Обработка загрузки изображений и их распознавания с использованием MobileNetV2.
"""

# Вспомогательная функция для распознавания объектов на изображении
def recognize_image(file_path):
    """
    Распознает объекты на изображении с использованием модели MobileNetV2.

    :param file_path: Путь к файлу изображения.
    :return: Список предсказаний (топ-3), содержащих класс, описание и вероятность.
    """
    # Загружаем предварительно обученную модель MobileNetV2
    model = MobileNetV2(weights='imagenet')

    # Загружаем изображение и изменяем его размер до 224x224 пикселей
    img = image.load_img(file_path, target_size=(224, 224))

    # Преобразуем изображение в массив numpy
    img_array = image.img_to_array(img)

    # Добавляем измерение (batch dimension)
    img_array = np.expand_dims(img_array, axis=0)

    # Предобрабатываем изображение
    img_array = preprocess_input(img_array)

    # Предсказание
    predictions = model.predict(img_array)

    # Декодируем предсказания
    decoded_predictions = decode_predictions(predictions, top=3)[0]

    return decoded_predictions


# Представление для главной страницы
def home_view(request):
    """
    Отображает главную страницу приложения.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с отрендеренным шаблоном.
    """
    return render(request, 'pusha/home.html')


# Представление для входа в систему
def login_view(request):
    """
    Обрабатывает вход пользователя в систему.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с отрендеренным шаблоном или перенаправление на dashboard.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Перенаправление на панель управления
        else:
            return HttpResponse("Invalid login credentials")
    return render(request, 'pusha/login.html')


# Представление для выхода из системы
def logout_view(request):
    """
    Обрабатывает выход пользователя из системы.

    :param request: Объект HTTP-запроса.
    :return: Перенаправление на главную страницу.
    """
    logout(request)
    return redirect('home')


# Представление для регистрации пользователя
def register_view(request):
    """
    Обрабатывает регистрацию нового пользователя.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с отрендеренным шаблоном или перенаправление на login.
    """
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different one.")
                return redirect('register')

            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "User registered successfully.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "An error occurred during registration. Please try again.")
            return redirect('register')

    return render(request, 'pusha/register.html')


# Представление для панели управления
@login_required
def dashboard_view(request):
    """
    Отображает панель управления для аутентифицированного пользователя.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с отрендеренным шаблоном панели управления.
    """
    context = {}
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']

            # Сохраняем загруженное изображение
            file_path = f'media/{image_file.name}'
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            # Распознаем объекты на изображении
            predictions = recognize_image(file_path)

            # Передаем предсказания в контекст
            context['predictions'] = predictions
    else:
        form = UploadImageForm()

    context['form'] = form
    return render(request, 'pusha/dashboard.html', context)


# Представление для добавления изображения в ленту
@login_required(login_url='login')
def add_image_feed_view(request):
    """
    Отображает страницу для добавления изображения в ленту.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с отрендеренным шаблоном.
    """
    return render(request, 'pusha/add_image_feed.html')


# Представление для распознавания объектов
@login_required(login_url='/object_detection/login')
def object_detection_view(request):
    """
    Отображает страницу для распознавания объектов на изображении.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с отрендеренным шаблоном.
    """
    return render(request, 'pusha/object_detection.html')


# Представление для перенаправления на страницу регистрации
def redirect_to_register(request):
    """
    Перенаправляет пользователя на страницу регистрации.

    :param request: Объект HTTP-запроса.
    :return: Перенаправление на URL регистрации.
    """
    return redirect('register')
@login_required
def dashboard(request):
    # Здесь ваша логика для дашборда
    return render(request, 'dashboard.html')