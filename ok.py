import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('default')


data = pd.read_csv("dataset_telemetry.csv")
data["timestamp"] = pd.to_datetime(data["timestamp"])

days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

data["hour"] = data["timestamp"].dt.hour
data["day"] = data["timestamp"].dt.weekday
data["month"] = data["timestamp"].dt.month

data["gender"] = data["gender"].apply(lambda x: (0, 1)[x == "Ж"])
#data["day"] = data["day"].apply(lambda x: days[x])

city_freq = data['city'].value_counts(normalize=True)
data['city_freq'] = data['city'].map(city_freq)
data['is_weekend'] = data['day'].isin([5, 6]).astype(int)


print(data.head(), end="\n\n\n")


print("Корреляционный анализ\n\n")

grades_cols = ["day", "hour", "month", "value", "age", "gender", "city_freq", "is_weekend"]
#"age", "category"
correlation_matrix = data[grades_cols].corr()

print("Корреляционная матрица оценок:")
print(correlation_matrix.round(3))

# Корреляция времени с действиями
time_corr = data.groupby('userid').agg({
    'hour': 'mean',
    'is_weekend': 'mean',
    'value': 'sum'
}).corr()


print("Корреляция времени с действиями\n\n")
print(time_corr)


print("Корреляции для категорий действий\n\n")
# One-hot encoding для категорий действий
action_dummies = pd.get_dummies(data['action'])
category_dummies = pd.get_dummies(data['category'])

# Объединение с исходными данными
df_encoded = pd.concat([data[['userid', 'age', 'value']], 
                       action_dummies, category_dummies], axis=1)

# Агрегация по пользователям и корреляция
user_actions = df_encoded.groupby('userid').mean()
corr_matrix = user_actions.corr().round(3)
# Найдем самые сильные корреляции
print("\nСАМЫЕ СИЛЬНЫЕ КОРРЕЛЯЦИИ:")
cols = list(user_actions.columns)
for i in range(len(cols)):
    for j in range(i+1, len(cols)):
        corr_value = corr_matrix.iloc[i, j]
        if abs(corr_value) > 0.3:  # Показываем только значимые корреляции
            print(f"{cols[i]} ↔ {cols[j]}: {corr_value:.3f}")

    

# Создаем тепловую карту корреляций
fig, ax = plt.subplots(figsize=(14, 9))

# Создаем тепловую карту
im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)

# Добавляем значения корреляций
for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                      ha="center", va="center", color="black", fontweight='bold')

# Настраиваем оси
ax.set_xticks(range(len(corr_matrix.columns)))
ax.set_yticks(range(len(corr_matrix.columns)))
ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
ax.set_yticklabels(corr_matrix.columns)

ax.set_title('Тепловая карта корреляций', fontsize=16, fontweight='bold')

# Добавляем цветовую шкалу
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Коэффициент корреляции', rotation=270, labelpad=20)

plt.tight_layout()
plt.show()

print("Тепловая карта создана! Красный цвет = положительная корреляция, синий = отрицательная.")