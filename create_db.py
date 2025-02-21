import sqlite3
import pandas as pd
import logging

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

def create_table(conn):
    """Создает таблицу wines в базе данных."""
    try:
        conn.execute("DROP TABLE IF EXISTS wines")
        create_table_query = """
        CREATE TABLE wines (
            id INTEGER PRIMARY KEY,
            country TEXT,
            description TEXT,
            designation TEXT,
            points INTEGER,
            price REAL,
            province TEXT,
            region_1 TEXT,
            region_2 TEXT,
            taster_name TEXT,
            taster_twitter_handle TEXT,
            title TEXT,
            variety TEXT,
            winery TEXT
        );
        """
        conn.execute(create_table_query)
        print("Таблица wines успешно создана!")
    except sqlite3.Error as e:
        logging.error(f"Ошибка при создании таблицы: {e}")

def import_data(conn):
    """Импортирует данные из CSV в таблицу wines."""
    try:
        df = pd.read_csv("winemag-data-130k-v2.csv")
        df.to_sql("wines", conn, if_exists="replace", index=False)
        print("Данные успешно загружены!")
    except Exception as e:
        logging.error(f"Ошибка при импорте данных: {e}")

def main():
    """Основная функция для создания базы данных и импорта данных."""
    try:
        with sqlite3.connect("wines.db") as conn:
            create_table(conn)
            import_data(conn)
    except sqlite3.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")

if __name__ == "__main__":
    main()