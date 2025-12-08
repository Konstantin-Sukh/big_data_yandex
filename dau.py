import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("dataset_telemetry.csv")

#преобразуем в datetime формат
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.day_name()
df['weekday_num'] = df['timestamp'].dt.weekday

min_date = df['timestamp'].min()
max_date = df['timestamp'].max()
date_range = max_date - min_date

#расчет dau
dau = df.groupby('date')['userid'].nunique()

#статистика пользователей
unique_users = df['userid'].nunique()
avg_dau = dau.mean()
min_dau = dau.min()
max_dau = dau.max()

#создаем тепловую карту
fig, ax = plt.subplots(figsize=(14, 8))

#уникальных пользователей по каждому дню отдельно
daily_unique_users = df.groupby(['date', 'day_of_week', 'hour'])['userid'].nunique().reset_index()
#усредняем 
pivot_data = daily_unique_users.groupby(['day_of_week', 'hour'])['userid'].mean().unstack(fill_value=0)

#подписи
weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
pivot_data = pivot_data.reindex(weekday)
days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

heatmap = sns.heatmap(pivot_data, cmap='YlOrRd', linewidths=0.5, linecolor='gray', cbar_kws={
        'label': 'Среднее количество уникальных пользователей',
        'shrink': 0.8}, ax=ax)

ax.set_yticklabels(days, rotation=0, fontsize=11)
ax.set_xlabel('Час дня', fontsize=12)
ax.set_ylabel('День недели', fontsize=12)

ax.set_title(
    f'Среднее количество уникальных пользователей по дням недели и часам\n'
    f'Всего пользователей: {unique_users} | Средний DAU: {avg_dau:.0f} | '
    f'Мин DAU: {min_dau} | Макс DAU: {max_dau}',
    fontsize=14,)

plt.tight_layout()


plt.show()
