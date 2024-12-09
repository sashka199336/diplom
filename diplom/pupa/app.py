from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Для работы flash-сообщений


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


def insert_user(email, password):
    """
    Вставляет нового пользователя в базу данных.
    Хэширует пароль перед сохранением.
    """
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    password_hash = generate_password_hash(password)  # Безопасное хэширование
    try:
        cur.execute('''
            INSERT INTO users (email, password_hash)
            VALUES (?, ?)
        ''', (email, password_hash))
        conn.commit()
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        cur.close()
        conn.close()
    return True, "User registered successfully."


def is_valid_email(email):
    """
    Проверяет, является ли email корректным.
    """
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Обрабатывает регистрацию пользователей.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not is_valid_email(email):
            flash("Invalid email format.", "error")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return redirect(url_for('register'))

        success, message = insert_user(email, password)
        if success:
            flash("Registration successful!", "success")
            return redirect(url_for('success'))
        else:
            flash(f"Error: {message}", "error")
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/success')
def success():
    """
    Страница успешной регистрации.
    """
    return "Registration successful!"


if __name__ == '__main__':
    create_table()
    app.run(debug=True)