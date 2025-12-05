import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("dataset_telemetry.csv")

df_cart = df[df['action'] == 'cart']

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
plt.subplots_adjust(hspace=0.8, wspace=0.5)

# по полу
gender_counts = df_cart['gender'].value_counts()
gender = gender_counts.index
vals = gender_counts.values

axes[0, 0].bar(gender, vals, color=['lightpink', 'lightblue'], edgecolor='black')
axes[0, 0].set_title('Распределение по полу', fontsize=14)
axes[0, 0].set_ylabel('Количество', fontsize=12)
axes[0, 0].grid(axis='y', alpha=0.3)

total = vals.sum()
for i, v in enumerate(vals):
    axes[0, 0].text(i, v/2, f'{v}\n({v/total*100:.1f}%)',
                    ha='center', va='center', fontsize=10, color='white')

# по городам
city_counts = df_cart['city'].value_counts().head(8)
cities = city_counts.index
counts = city_counts.values

axes[1, 0].bar(cities, counts, color='skyblue', edgecolor='blue')
axes[1, 0].set_title('Топ-8 городов')
axes[1, 0].set_ylabel('Количество добавлений в корзину')
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].grid(axis='y', alpha=0.3)

total = counts.sum()
for i, v in enumerate(counts):
    axes[1, 0].text(i, v/2, f'{v}\n({v/total*100:.1f}%)',
                    ha='center', va='center', fontsize=9, color='white')

# по категориям
category_counts = df_cart['category'].value_counts().head(8)
cats = category_counts.index
vals = category_counts.values

axes[0, 1].bar(cats, vals, color='lightgreen', edgecolor='black')
axes[0, 1].set_title('Топ-8 категорий', fontsize=14)
axes[0, 1].set_ylabel('Количество добавлений в корзину', fontsize=12)
axes[0, 1].tick_params(axis='x', rotation=45)
axes[0, 1].grid(axis='y', alpha=0.3)

total = vals.sum()
for i, v in enumerate(vals):
    axes[0, 1].text(i, v/2, f'{v}\n({v/total*100:.1f}%)',
                    ha='center', va='center', fontsize=9, color='white')

axes[1, 1].axis('off')

plt.tight_layout()
plt.show()


# по стоимости покупки
def categorize_price(value):
    if value < 100:
        return 'Очень дешевые (<100 руб)'
    elif value < 500:
        return 'Дешевые (100-500 руб)'
    elif value < 1000:
        return 'Бюджетные (500-1000 руб)'
    elif value < 5000:
        return 'Средние (1000-5000 руб)'
    elif value < 10000:
        return 'Дорогие (5000-10000 руб)'
    elif value < 50000:
        return 'Очень дорогие (10000-50000 руб)'
    else:
        return 'Премиум (>50000 руб)'

df2 = df[df['action'] == 'confirmation'].copy()
df2['price_category'] = df2['value'].apply(categorize_price)

price_counts = df2['price_category'].value_counts()

category_order = [
    'Очень дешевые (<100 руб)',
    'Дешевые (100-500 руб)',
    'Бюджетные (500-1000 руб)',
    'Средние (1000-5000 руб)',
    'Дорогие (5000-10000 руб)',
    'Очень дорогие (10000-50000 руб)',
    'Премиум (>50000 руб)'
]

sorted_vals = [price_counts.get(cat, 0) for cat in category_order]

plt.figure(figsize=(12, 6))
bars = plt.bar(category_order, sorted_vals, color='lightpink', edgecolor='deeppink')

plt.title('Распределение покупок по ценовым категориям', fontsize=16)
plt.ylabel('Количество покупок', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)

total = sum(sorted_vals)
for i, v in enumerate(sorted_vals):
    plt.text(i, v/2, f'{v}\n({v/total*100:.1f}%)',
             ha='center', va='center', fontsize=9, color='white')

plt.tight_layout()
plt.show()


# средний возраст по полу
avg_age = df2.groupby('gender')['age'].mean()

plt.figure(figsize=(6, 4))
plt.bar(avg_age.index, avg_age.values, color=['lightpink', 'lightblue'], edgecolor='black')
plt.title('Средний возраст покупателей по полу', fontsize=14)
plt.ylabel('Возраст', fontsize=12)
plt.grid(axis='y', alpha=0.3)

for i, v in enumerate(avg_age.values):
    plt.text(i, v/2, f'{v:.1f}', ha='center', va='center', color='white')

plt.show()



