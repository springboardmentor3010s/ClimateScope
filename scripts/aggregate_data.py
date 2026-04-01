import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_weather.csv")

# Convert date column
df['last_updated'] = pd.to_datetime(df['last_updated'])

# Set date as index
df.set_index('last_updated', inplace=True)

# Select only numeric columns for aggregation
numeric_df = df.select_dtypes(include=['float64', 'int64'])

# Monthly average
monthly_df = numeric_df.resample('ME').mean()

# Save result
monthly_df.to_csv("data/processed/monthly_weather.csv")

print("Monthly dataset created successfully!")
