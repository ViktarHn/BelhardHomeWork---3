import pandas as pd
import logging

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

def clean_data():
    """Очищает данные от пропусков и дубликатов."""
    try:
        df = pd.read_csv('winemag-data-130k-v2.csv')
        
        # Проверка на пропуски
        print("Пропуски в данных:")
        print(df.isnull().sum())
        
        # Проверка на дубликаты
        print("Количество дубликатов:", df.duplicated().sum())
        
        # Удаление дубликатов
        df = df.drop_duplicates()
        
        # Удаление строк с пропусками в ключевых столбцах
        df = df.dropna(subset=['points', 'price'])
        
        # Проверка структуры данных
        print("Информация о данных после очистки:")
        print(df.info())
    except Exception as e:
        logging.error(f"Ошибка при очистке данных: {e}")

if __name__ == "__main__":
    clean_data()