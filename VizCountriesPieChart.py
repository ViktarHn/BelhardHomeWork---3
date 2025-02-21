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

def visualize_data(data, title, save_path=None):
    """Визуализирует данные и сохраняет график."""
    plt.figure(figsize=(8, 8))
    plt.pie(data['count'], labels=data['country'], autopct='%1.1f%%', startangle=140)
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    plt.show()

def main():
    """Основная функция для визуализации распределения вин по странам."""
    try:
        with sqlite3.connect('wines.db') as conn:
            query = '''
            SELECT country, COUNT(*) as count FROM wines GROUP BY country ORDER BY count DESC LIMIT 10;
            '''
            data = execute_query(conn, query)
            if data:
                df = pd.DataFrame(data, columns=['country', 'count'])
                visualize_data(df, 'Доля вин по странам (Топ-10)', 'plots/pie_chart_country_distribution.png')
    except sqlite3.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")

if __name__ == "__main__":
    main()