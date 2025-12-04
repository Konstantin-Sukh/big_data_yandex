import polars as pl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import numpy as np

plt.style.use('default')
rcParams['figure.figsize'] = (12, 8)
rcParams['font.size'] = 12


data = pl.read_csv("dataset_telemetry.csv")
data = data.with_columns(
    pl.col("timestamp").str.to_datetime("%Y-%m-%dT%H:%M:%S")
)
print(data.describe())

data["value"].value_counts().sort(by='count')

print(data.filter(pl.col("value") == max(data["value"])))


for el in data.columns:
    print("СТОЛБЕЦ:", el, '\n', data[el].value_counts().sort(by="count"))