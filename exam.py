import sqlite3
import logging

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

def check_database():
    """Проверяет структуру и содержимое базы данных."""
    try:
        with sqlite3.connect("wines.db") as conn:
            cursor = conn.cursor()
            
            # Проверка структуры
            cursor.execute("PRAGMA table_info(wines);")
            print("Структура таблицы:", cursor.fetchall())
            
            # Проверка количества записей
            cursor.execute("SELECT COUNT(*) FROM wines;")
            print("Количество записей:", cursor.fetchone()[0])
            
            # Первые 5 записей
            cursor.execute("SELECT * FROM wines LIMIT 5;")
            print("Первые 5 записей:", cursor.fetchall())
    except sqlite3.Error as e:
        logging.error(f"Ошибка при проверке базы данных: {e}")

if __name__ == "__main__":
    check_database()