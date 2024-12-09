from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

# Список слов для угадывания
words = ["python", "fastapi", "hangman", "developer", "programming"]

# Глобальное хранилище состояния игры (для упрощения)
game_state = {
    "word": None,
    "guessed_letters": [],
    "remaining_attempts": 6,
    "current_display": "",
    "game_over": False,
    "win": False
}


class GuessRequest(BaseModel):
    """
    Модель для валидации данных при угадывании буквы.

    Атрибуты:
        letter (str): Буква, отправленная клиентом.
    """
    letter: str


def start_new_game():
    """
    Запускает новую игру, устанавливая начальное состояние для глобального объекта game_state.
    """
    word = random.choice(words)  # Выбираем случайное слово
    game_state["word"] = word
    game_state["guessed_letters"] = []
    game_state["remaining_attempts"] = 6
    game_state["current_display"] = "_" * len(word)
    game_state["game_over"] = False
    game_state["win"] = False


def update_display():
    """
    Обновляет текущее отображение слова, заменяя символы "_" на угаданные буквы.
    """
    word = game_state["word"]
    guessed_letters = game_state["guessed_letters"]
    game_state["current_display"] = "".join(
        [letter if letter in guessed_letters else "_" for letter in word]
    )


def check_game_status():
    """
    Проверяет состояние игры (выигрыш или проигрыш) и обновляет соответствующие флаги game_state.
    """
    if "_" not in game_state["current_display"]:
        game_state["game_over"] = True
        game_state["win"] = True
    elif game_state["remaining_attempts"] <= 0:
        game_state["game_over"] = True
        game_state["win"] = False


@app.post("/start")
def start_game():
    """
    Эндпоинт для начала новой игры.

    Возвращает:
        dict: Сообщение, текущее отображение слова и оставшиеся попытки.
    """
    start_new_game()
    return {
        "message": "New game started!",
        "current_display": game_state["current_display"],
        "remaining_attempts": game_state["remaining_attempts"]
    }


@app.post("/guess")
def guess_letter(request: GuessRequest):
    """
    Эндпоинт для угадывания буквы.

    Параметры:
        request (GuessRequest): Запрос, содержащий букву.

    Возвращает:
        dict: Текущее отображение слова, оставшиеся попытки, статус игры и информацию о победе.

    Исключения:
        HTTPException: Если игра уже закончена, буква недействительна или уже была угадана.
    """
    if game_state["game_over"]:
        raise HTTPException(status_code=400, detail="Game is already over. Start a new game.")

    letter = request.letter.lower()

    # Проверка правильности ввода
    if len(letter) != 1 or not letter.isalpha():
        raise HTTPException(status_code=400, detail="Invalid letter. Please provide a single alphabetic character.")

    if letter in game_state["guessed_letters"]:
        raise HTTPException(status_code=400, detail="Letter already guessed.")

    # Добавление буквы в список угаданных
    game_state["guessed_letters"].append(letter)

    # Проверка, есть ли буква в слове
    if letter in game_state["word"]:
        update_display()
    else:
        game_state["remaining_attempts"] -= 1

    # Проверка состояния игры (выигрыш/проигрыш)
    check_game_status()

    return {
        "current_display": game_state["current_display"],
        "remaining_attempts": game_state["remaining_attempts"],
        "game_over": game_state["game_over"],
        "win": game_state["win"]
    }


@app.get("/state")
def get_game_state():
    """
    Эндпоинт для получения текущего состояния игры.

    Возвращает:
        dict: Текущее отображение слова, оставшиеся попытки, список угаданных букв,
        статус игры и информацию о победе.
    """
    return {
        "current_display": game_state["current_display"],
        "remaining_attempts": game_state["remaining_attempts"],
        "guessed_letters": game_state["guessed_letters"],
        "game_over": game_state["game_over"],
        "win": game_state["win"]
    }


@app.get("/")
def root():
    """
    Эндпоинт для приветствия.

    Возвращает:
        dict: Сообщение с информацией о доступности документации по API.
    """
    return {"message": "Welcome to the Hangman API! Use /docs to explore the API."}