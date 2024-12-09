import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

"""
Модуль для классификации изображений и обнаружения объектов
с использованием MobileNetV2 (TensorFlow/Keras) и Caffe (OpenCV).
"""

def recognize_image(file_path):
    """
    Классификация изображения с использованием модели MobileNetV2.

    Аргументы:
        file_path (str): Путь к изображению.

    Возвращает:
        list: Список топ-3 предсказаний в формате (класс, название, вероятность).
    """
    # Загрузка предобученной модели MobileNetV2
    model = MobileNetV2(weights='imagenet')

    # Загрузка и предварительная обработка изображения
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Прогнозирование
    predictions = model.predict(img_array)

    # Декодирование предсказаний
    decoded_predictions = decode_predictions(predictions, top=3)[0]

    return decoded_predictions


def process_image(image_path):
    """
    Обнаружение объектов на изображении с использованием модели Caffe.

    Аргументы:
        image_path (str): Путь к изображению.

    Возвращает:
        list: Список обнаруженных объектов, содержащий метки классов и координаты ограничивающих рамок.
    """
    # Загрузка модели Caffe
    net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')

    # Загрузка изображения
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]

    # Подготовка блоба (blob) из изображения
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)),
        0.007843,
        (300, 300),
        127.5
    )

    # Передача блоба в сеть
    net.setInput(blob)
    detections = net.forward()

    # Обработка обнаруженных объектов
    results = []
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]  # Уверенность предсказания
        if confidence > 0.2:  # Фильтрация по порогу уверенности
            idx = int(detections[0, 0, i, 1])  # Индекс класса
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])  # Координаты рамки
            (startX, startY, endX, endY) = box.astype("int")
            label = f"Class {idx}: {confidence:.2f}"  # Метка с классом и уверенностью
            results.append((label, (startX, startY, endX, endY)))

    return results