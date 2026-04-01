import pandas as pd

df = pd.read_csv("data/raw/GlobalWeatherRepository.csv")

print("\nColumns:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())
