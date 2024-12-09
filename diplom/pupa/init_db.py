import sqlite3

def get_connection(db_name='example.db'):
    """
    Устанавливает соединение с базой данных SQLite.
    :param db_name: Имя файла базы данных.
    :return: Объект соединения.
    """
    return sqlite3.connect(db_name)

def create_table():
    """
    Создаёт таблицу users в базе данных, если она ещё не существует.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
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
        print("Table 'users' created or already exists.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating the table: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    create_table()