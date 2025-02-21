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

def visualize_histogram(data, x_label, y_label, title, save_path=None):
    """Визуализирует гистограмму и сохраняет график."""
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

def visualize_pie_chart(data, title, save_path=None):
    """Визуализирует круговую диаграмму и сохраняет график."""
    plt.figure(figsize=(8, 8))
    plt.pie(data['count'], labels=data['country'], autopct='%1.1f%%', startangle=140)
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    plt.show()

def main():
    """Основная функция для визуализации распределения цен и вин по странам."""
    try:
        with sqlite3.connect('wines.db') as conn:
            # Запрос для гистограммы
            price_query = '''
            SELECT country, price FROM wines WHERE price IS NOT NULL AND country IN (
                SELECT country FROM wines GROUP BY country HAVING COUNT(*) > 1000
            );
            '''
            price_data = execute_query(conn, price_query)
            if price_data:
                df_prices = pd.DataFrame(price_data, columns=['country', 'price'])
                visualize_histogram(df_prices, 'Цена (price)', 'Частота', 'Распределение цен по странам', 'plots/price_distribution_by_country.png')

            # Запрос для круговой диаграммы
            country_query = '''
            SELECT country, COUNT(*) as count FROM wines GROUP BY country ORDER BY count DESC LIMIT 10;
            '''
            country_data = execute_query(conn, country_query)
            if country_data:
                df_countries = pd.DataFrame(country_data, columns=['country', 'count'])
                visualize_pie_chart(df_countries, 'Доля вин по странам (Топ-10)', 'plots/pie_chart_country_distribution.png')
    except sqlite3.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")

if __name__ == "__main__":
    main()