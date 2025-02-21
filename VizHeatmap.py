import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import logging

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

# Создание папки для графиков
if not os.path.exists('plots'):
    os.makedirs('plots')

def fetch_data():
    """Извлекает данные для построения тепловой карты корреляции."""
    try:
        conn = sqlite3.connect('wines.db')
        query = '''
        SELECT points, price FROM wines WHERE points IS NOT NULL AND price IS NOT NULL;
        '''
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        logging.error(f"Ошибка при извлечении данных: {e}")
        return None

def visualize_heatmap(df):
    """Визуализирует тепловую карту корреляции."""
    try:
        plt.figure(figsize=(8, 6))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
        plt.title('Тепловая карта корреляции между оценками и ценами')
        plt.savefig('plots/heatmap_correlation.png')  # Сохранение графика
        plt.show()
    except Exception as e:
        logging.error(f"Ошибка при визуализации данных: {e}")

if __name__ == "__main__":
    df = fetch_data()
    if df is not None:
        visualize_heatmap(df)