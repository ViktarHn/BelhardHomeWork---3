import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import logging

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

# Создание папки для графиков, если она не существует
if not os.path.exists('plots'):
    os.makedirs('plots')

def fetch_data():
    """Извлекает данные из базы данных для топ-10 самых дорогих вин."""
    try:
        conn = sqlite3.connect('wines.db')
        query = '''
        SELECT title, price FROM wines WHERE price IS NOT NULL ORDER BY price DESC LIMIT 10;
        '''
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        logging.error(f"Ошибка при извлечении данных: {e}")
        return None

def visualize_data(df):
    """Визуализирует топ-10 самых дорогих вин."""
    try:
        plt.figure(figsize=(10, 6))
        plt.barh(df['title'], df['price'], color='skyblue')
        plt.title('Топ-10 самых дорогих вин')
        plt.xlabel('Цена (price)')
        plt.ylabel('Название вина')
        plt.savefig('plots/top_10_expensive_wines.png')  # Сохранение графика
        plt.show()
    except Exception as e:
        logging.error(f"Ошибка при визуализации данных: {e}")

if __name__ == "__main__":
    df = fetch_data()
    if df is not None:
        visualize_data(df)