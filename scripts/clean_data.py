import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/GlobalWeatherRepository.csv")

print("Original shape:", df.shape)

# -------------------------
# Convert last_updated column
# -------------------------
if 'last_updated' in df.columns:
    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')

# -------------------------
# Remove duplicates
# -------------------------
df = df.drop_duplicates()

# -------------------------
# Fill missing numeric values
# -------------------------
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].mean())

print("After cleaning:", df.shape)

# -------------------------
# Save cleaned dataset
# -------------------------
df.to_csv("data/processed/cleaned_weather.csv", index=False)

print("Cleaned dataset saved.")
