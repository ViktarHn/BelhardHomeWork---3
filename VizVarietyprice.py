import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Создание папки для графиков, если она не существует
if not os.path.exists('plots'):
    os.makedirs('plots')

conn = sqlite3.connect('wines.db')
query = '''
SELECT variety, price FROM wines 
WHERE variety IN (
    SELECT variety FROM wines GROUP BY variety HAVING COUNT(*) > 500
) AND price IS NOT NULL;
'''
df = pd.read_sql(query, conn)

plt.figure(figsize=(12, 8))
sns.violinplot(x='variety', y='price', data=df)
plt.title('Распределение цен по сортам винограда')
plt.xlabel('Сорт винограда')
plt.ylabel('Цена (price)')
plt.xticks(rotation=90)
plt.savefig('plots/violin_price_by_variety.png')  # Сохранение графика
plt.show()

conn.close()