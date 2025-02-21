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
    """Извлекает данные из базы данных для анализа зависимости цены от оценки."""
    try:
        conn = sqlite3.connect('wines.db')
        query = '''
        SELECT points, price FROM wines
        WHERE price IS NOT NULL AND points IS NOT NULL;
        '''
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        logging.error(f"Ошибка при извлечении данных: {e}")
        return None

def visualize_data(df):
    """Визуализирует зависимость цены от оценки."""
    try:
        plt.figure(figsize=(10, 6))
        plt.scatter(df['points'], df['price'], alpha=0.5)
        plt.title('Оценка vs. Цена')
        plt.xlabel('Оценка (points)')
        plt.ylabel('Цена (price)')
        plt.grid(True)
        plt.savefig('plots/points_vs_price.png')  # Сохранение графика
        plt.show()
    except Exception as e:
        logging.error(f"Ошибка при визуализации данных: {e}")

if __name__ == "__main__":
    df = fetch_data()
    if df is not None:
        visualize_data(df)