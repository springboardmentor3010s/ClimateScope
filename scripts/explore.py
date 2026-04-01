import pandas as pd

df = pd.read_csv("data/raw/GlobalWeatherRepository.csv")

print("Dataset loaded successfully")
print(df.head())
print(df.shape)
