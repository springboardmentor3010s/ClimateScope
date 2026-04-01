import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_weather.csv")

# Convert date
df['last_updated'] = pd.to_datetime(df['last_updated'])

print("Statistical Summary:\n")
print(df.describe())

# Temperature distribution
plt.figure()
sns.histplot(df['temperature_celsius'], bins=30)
plt.title("Temperature Distribution")
plt.xlabel("Temperature (°C)")
plt.ylabel("Frequency")
plt.show()

# -------------------------------
# Monthly Temperature Trend
# -------------------------------

# Set date as index
df.set_index('last_updated', inplace=True)

# Monthly average temperature
monthly_temp = df['temperature_celsius'].resample('ME').mean()

plt.figure()
monthly_temp.plot()
plt.title("Monthly Average Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.show()

# -------------------------------
# Correlation Heatmap (Improved)
# -------------------------------

plt.figure(figsize=(12, 10))

# Select only important weather columns
selected_columns = [
    'temperature_celsius',
    'wind_kph',
    'humidity',
    'pressure_mb',
    'precip_mm'
]

available_columns = [col for col in selected_columns if col in df.columns]

corr = df[available_columns].corr()

sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Between Key Weather Variables")
plt.show()

# -------------------------------
# Extreme Weather Detection
# -------------------------------

# Extreme heat (> 40°C)
extreme_heat = df[df['temperature_celsius'] > 40]
print("\nExtreme Heat Records:", len(extreme_heat))

# Extreme cold (< -10°C)
extreme_cold = df[df['temperature_celsius'] < -10]
print("Extreme Cold Records:", len(extreme_cold))

# High wind (> 60 kph)
extreme_wind = df[df['wind_kph'] > 60]
print("Extreme Wind Records:", len(extreme_wind))

# -------------------------------
# Country Comparison
# -------------------------------

country_avg_temp = df.groupby('country')['temperature_celsius'].mean().sort_values(ascending=False)

print("\nTop 5 Hottest Countries:")
print(country_avg_temp.head())

print("\nTop 5 Coldest Countries:")
print(country_avg_temp.tail())