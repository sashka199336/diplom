import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash

def create_table():
    """
    Создаёт таблицу users в базе данных, если она ещё не существует.
    """
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.commit()
    cur.close()
    conn.close()


def is_valid_email(email):
    """
    Проверяет корректность email-адреса с использованием регулярного выражения.
    """
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


def insert_user(email, password):
    """
    Добавляет нового пользователя в базу данных.
    Хэширует пароль перед сохранением.

    :param email: Email пользователя
    :param password: Пароль пользователя
    :return: Статус добавления (успех или ошибка)
    """
    if not is_valid_email(email):
        return False, "Invalid email format."

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    conn = sqlite3.connect('example.db')
    cur = conn.cursor()

    # Безопасное хэширование пароля
    password_hash = generate_password_hash(password)

    try:
        cur.execute('''
            INSERT INTO users (email, password_hash)
            VALUES (?, ?)
        ''', (email, password_hash))
        conn.commit()
    except sqlite3.IntegrityError as e:
        return False, f"Error inserting user: {e}"
    finally:
        cur.close()
        conn.close()

    return True, "User inserted successfully."


if __name__ == '__main__':
    create_table()

    # Пример добавления пользователя
    email = 'user@example.com'
    password = 'securepassword'
    success, message = insert_user(email, password)
    print(message)