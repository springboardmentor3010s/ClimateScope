import pandas as pd

def load_data():
    df = pd.read_csv("GlobalWeather_Preprocessed.csv")

    # Normalize values (0–1 scale)
    df["temp_norm"] = (df["temperature_celsius"] - df["temperature_celsius"].min()) / (
        df["temperature_celsius"].max() - df["temperature_celsius"].min()
    )

    df["humidity_norm"] = (df["humidity"] - df["humidity"].min()) / (
        df["humidity"].max() - df["humidity"].min()
    )

    df["wind_norm"] = (df["wind_kph"] - df["wind_kph"].min()) / (
        df["wind_kph"].max() - df["wind_kph"].min()
    )

    # Risk Score (weighted)
    df["risk_score"] = (
        0.5 * df["temp_norm"] +
        0.3 * df["humidity_norm"] +
        0.2 * df["wind_norm"]
    )

    # Risk Category
    def classify(score):
        if score > 0.7:
            return "High"
        elif score > 0.4:
            return "Medium"
        else:
            return "Low"

    df["risk_level"] = df["risk_score"].apply(classify)

    return df