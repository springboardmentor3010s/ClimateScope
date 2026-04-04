import streamlit as st

def apply_filters(df):

    st.sidebar.header("🔍 Advanced Filters")

    country = st.sidebar.multiselect(
        "🌍 Country",
        df["country"].unique(),
        default=df["country"].unique()
    )

    condition = st.sidebar.multiselect(
        "☁ Weather Condition",
        df["condition_text"].unique(),
        default=df["condition_text"].unique()
    )

    temp_range = st.sidebar.slider(
        "🌡 Temperature",
        float(df["temperature_celsius"].min()),
        float(df["temperature_celsius"].max()),
        (
            float(df["temperature_celsius"].min()),
            float(df["temperature_celsius"].max())
        )
    )

    humidity_range = st.sidebar.slider(
        "💧 Humidity",
        float(df["humidity"].min()),
        float(df["humidity"].max()),
        (
            float(df["humidity"].min()),
            float(df["humidity"].max())
        )
    )

    search = st.sidebar.text_input("🔎 Search Location")

    df = df[
        (df["country"].isin(country)) &
        (df["condition_text"].isin(condition)) &
        (df["temperature_celsius"].between(*temp_range)) &
        (df["humidity"].between(*humidity_range))
    ]

    if search:
        df = df[df["location_name"].str.contains(search, case=False)]

    return df