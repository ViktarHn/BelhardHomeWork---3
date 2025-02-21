import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import logging

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

# Создание папки для графиков
if not os.path.exists('plots'):
    os.makedirs('plots')

def execute_query(conn, query):
    """Выполняет SQL-запрос и возвращает результат."""
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при выполнении SQL-запроса: {e}")
        return None

def visualize_data(data, x_label, y_label, title, save_path=None):
    """Визуализирует данные и сохраняет график."""
    plt.figure(figsize=(10, 6))
    plt.scatter(data['points'], data['price'], alpha=0.5, label='Цена vs. Оценка')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path)
    plt.show()

def main():
    """Основная функция для анализа данных."""
    try:
        with sqlite3.connect('wines.db') as conn:
            query = '''
            SELECT points, price FROM wines 
            WHERE price IS NOT NULL AND points IS NOT NULL;
            '''
            data = execute_query(conn, query)
            if data:
                df = pd.DataFrame(data, columns=['points', 'price'])
                visualize_data(df, 'Оценка (points)', 'Цена (price)', 'Зависимость цены от оценки', 'plots/points_vs_price.png')
    except sqlite3.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")

if __name__ == "__main__":
    main()