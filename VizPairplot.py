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
    """Извлекает данные для построения pairplot."""
    try:
        conn = sqlite3.connect('wines.db')
        query = '''
        SELECT points, price, country FROM wines 
        WHERE points IS NOT NULL AND price IS NOT NULL AND country IS NOT NULL
        LIMIT 1000;  -- Ограничение для ускорения визуализации
        '''
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        logging.error(f"Ошибка при извлечении данных: {e}")
        return None

def visualize_pairplot(df):
    """Визуализирует pairplot для анализа взаимосвязей между переменными."""
    try:
        # Убедимся, что данные не пустые
        if df.empty:
            logging.error("Данные для визуализации отсутствуют.")
            return

        # Построение pairplot
        sns.pairplot(df, hue='country', diag_kind='kde')
        plt.suptitle('Pairplot для анализа взаимосвязей между оценками, ценами и странами')
        plt.savefig('plots/pairplot_analysis.png')  # Сохранение графика
        plt.show()
    except Exception as e:
        logging.error(f"Ошибка при визуализации данных: {e}")

if __name__ == "__main__":
    df = fetch_data()
    if df is not None:
        visualize_pairplot(df)