import sqlite3
import pandas as pd
import logging

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

def import_data():
    """Импортирует данные из CSV в базу данных."""
    try:
        df = pd.read_csv('winemag-data-130k-v2.csv')
        with sqlite3.connect('wines.db') as conn:
            df.to_sql('wines', conn, if_exists='replace', index=False)
        print("Данные успешно импортированы в базу данных.")
    except Exception as e:
        logging.error(f"Ошибка при импорте данных: {e}")

if __name__ == "__main__":
    import_data()