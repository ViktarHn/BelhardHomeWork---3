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
    plt.figure(figsize=(12, 8))
    for country in data['country'].unique():
        plt.hist(data[data['country'] == country]['price'], bins=30, alpha=0.5, label=country)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def main():
    """Основная функция для визуализации распределения цен по странам."""
    try:
        with sqlite3.connect('wines.db') as conn:
            query = '''
            SELECT country, price FROM wines WHERE price IS NOT NULL AND country IN (
                SELECT country FROM wines GROUP BY country HAVING COUNT(*) > 1000
            );
            '''
            data = execute_query(conn, query)
            if data:
                df = pd.DataFrame(data, columns=['country', 'price'])
                visualize_data(df, 'Цена (price)', 'Частота', 'Распределение цен по странам', 'plots/price_distribution_by_country.png')
    except sqlite3.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")

if __name__ == "__main__":
    main()