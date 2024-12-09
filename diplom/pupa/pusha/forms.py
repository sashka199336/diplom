from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ImageFeed, ImageUpload

"""
Формы для работы с пользователями и изображениями.

Этот файл содержит формы для создания пользователей, загрузки изображений
и взаимодействия с моделями `ImageFeed` и `ImageUpload`.
"""

# Форма для создания нового пользователя с обязательным полем email
class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя с добавлением поля email.
    """
    email = forms.EmailField(
        required=True,
        help_text='Обязательное поле. Введите действительный адрес электронной почты.'
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        """
        Сохраняет нового пользователя с введенным email.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# Форма для работы с моделью ImageFeed
class ImageFeedForm(forms.ModelForm):
    """
    Форма для загрузки изображений в модель ImageFeed.
    """
    class Meta:
        model = ImageFeed
        fields = ['image']


# Форма для работы с моделью ImageUpload
class ImageUploadForm(forms.ModelForm):
    """
    Форма для загрузки изображений в модель ImageUpload.
    """
    class Meta:
        model = ImageUpload
        fields = ['image']


# Простая форма для загрузки изображения (без привязки к модели)
class UploadImageForm(forms.Form):
    """
    Форма для загрузки изображения без использования модели.
    """
    image = forms.ImageField(label='Выберите изображение')