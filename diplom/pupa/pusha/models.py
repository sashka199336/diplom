from django.db import models
from django.contrib.auth.models import User

"""
Модели для работы с изображениями.

Этот файл содержит модели `ImageFeed` и `ImageUpload`, которые используются
для хранения информации о загружаемых изображениях, их обработке и результатах.
"""

class ImageFeed(models.Model):
    """
    Модель для хранения изображений, связанных с пользователем, и результата их обработки.

    Атрибуты:
        user: Пользователь, который загрузил изображение.
        image: Исходное изображение, загруженное пользователем.
        processed_image: Обработанное изображение, если доступно.
        result: Текстовой результат обработки изображения (например, результат анализа).
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name="Исходное изображение"
    )
    processed_image = models.ImageField(
        upload_to='processed_images/',
        blank=True,
        null=True,
        verbose_name="Обработанное изображение"
    )
    result = models.TextField(
        blank=True,
        null=True,
        verbose_name="Результат обработки"
    )

    def __str__(self):
        return f"Изображение пользователя {self.user.username}"


class ImageUpload(models.Model):
    """
    Модель для хранения загружаемых изображений.

    Атрибуты:
        image: Загружаемое изображение.
        uploaded_at: Дата и время загрузки изображения.
    """
    image = models.ImageField(
        upload_to='images/',
        verbose_name="Загруженное изображение"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки"
    )

    def __str__(self):
        return f"Изображение загружено {self.uploaded_at}"