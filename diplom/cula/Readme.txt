cula
cula — это веб-приложение, которое позволяет выполнять базовые математические вычисления. Приложение разработано на Flask (Python) и предоставляет простой и удобный интерфейс для пользователя.

Описание
Калькулятор поддерживает следующие функции:

Сложение (+)
Вычитание (-)
Умножение (*)
Деление (/)
Возведение в степень (x^y)
Вычисление процентов (%)
Очистка экрана (C)
Выражения вычисляются на серверной стороне с использованием Flask. Результат отображается на экране в реальном времени.

Установка
Требования
Python 3.7 или выше
Flask библиотека
Шаги запуска:
1.Скачайте проект
2.Через PyCharm зайдите в папку проекта
3.В терминале вбейте команду  'python app.py'
4.После запуска проекта перейдите по ссылке http://127.0.0.1:5000




Пример использования
Откройте приложение в браузере.
Используйте кнопки калькулятора для ввода математического выражения.
Нажмите "=" для вычисления результата.
Результат будет отображён на экране.
Основные файлы
app.py
Это основной файл приложения, который реализует серверную логику с использованием Flask. Он содержит два маршрута:

/ — отображает пользовательский интерфейс калькулятора.
/calculate (POST) — получает математическое выражение от клиента, вычисляет его и возвращает результат.
calculator.html
HTML-файл, который определяет пользовательский интерфейс калькулятора. Он включает в себя кнопки для ввода чисел и операций, а также поле для отображения результатов.

style.css
CSS-файл, отвечающий за стилизацию калькулятора. Вы можете изменить цвет кнопок, фон и другие стили в этом файле.



