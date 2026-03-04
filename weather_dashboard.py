import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="Global Weather Analysis", layout="wide")

# ----------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------
page = st.sidebar.radio("Navigation", ["Welcome", "Milestone 2 Dashboard"])

# ==========================================================
# 🏠 WELCOME PAGE
# ==========================================================
if page == "Welcome":

    st.markdown("""
    <h1 style='text-align:center; font-size:55px; color:#0072ff;'>
    🌍 Global Weather Analysis
    </h1>
    <h3 style='text-align:center; color:gray;'>
    Milestone 2: Core Analysis & Visualization Design
    </h3>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.write("""
    This interactive dashboard presents statistical analysis,
    trend analysis, extreme event detection, and regional comparisons
    using global weather data.
    """)

    st.markdown("---")
    st.info("Use the sidebar to open the Milestone 2 Dashboard.")

# ==========================================================
# 📊 MILESTONE 2 DASHBOARD
# ==========================================================
elif page == "Milestone 2 Dashboard":

    st.title("📊 Milestone 2: Core Analysis Dashboard")

    # ----------------------------------------------------------
    # LOAD DATA
    # ----------------------------------------------------------
    @st.cache_data
    def load_data():
        df = pd.read_csv("global_weather_cleaned.csv")
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        df["date_only"] = df["last_updated"].dt.date
        df["month"] = df["last_updated"].dt.month
        df["year"] = df["last_updated"].dt.year
        return df

    df = load_data()

    # ----------------------------------------------------------
    # FILTERS
    # ----------------------------------------------------------
    st.sidebar.header("Filters")

    country = st.sidebar.selectbox("Select Country",
                                   sorted(df["country"].unique()))

    min_date = df["date_only"].min()
    max_date = df["date_only"].max()

    date_range = st.sidebar.date_input("Select Date Range",
                                       (min_date, max_date))

    filtered_df = df[
        (df["country"] == country) &
        (df["date_only"] >= date_range[0]) &
        (df["date_only"] <= date_range[1])
    ]

    if filtered_df.empty:
        st.warning("No data available for selected filters.")
        st.stop()

    # ==========================================================
    # 1️⃣ STATISTICAL SUMMARY
    # ==========================================================
    st.header("1️⃣ Statistical Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Temperature",
                round(filtered_df["temperature_celsius"].mean(), 2))
    col2.metric("Avg Humidity",
                round(filtered_df["humidity"].mean(), 2))
    col3.metric("Avg Wind Speed",
                round(filtered_df["wind_kph"].mean(), 2))
    col4.metric("Avg Pressure",
                round(filtered_df["pressure_mb"].mean(), 2))

    st.write(filtered_df.describe())

    # ==========================================================
    # 2️⃣ CORRELATION ANALYSIS
    # ==========================================================
    st.header("2️⃣ Correlation Analysis")

    numeric_cols = [
        'temperature_celsius',
        'humidity',
        'wind_kph',
        'pressure_mb',
        'precip_mm',
        'visibility_km',
        'uv_index'
    ]

    corr = filtered_df[numeric_cols].corr()

    fig1, ax1 = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax1)
    st.pyplot(fig1)

    # ==========================================================
    # 3️⃣ SEASONAL PATTERNS & TRENDS
    # ==========================================================
    st.header("3️⃣ Seasonal Trends")

    monthly_avg = (
        filtered_df
        .groupby("month")["temperature_celsius"]
        .mean()
    )

    fig2, ax2 = plt.subplots()
    monthly_avg.plot(kind="bar", ax=ax2)
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Avg Temperature")
    st.pyplot(fig2)

    # ==========================================================
    # 4️⃣ EXTREME WEATHER EVENTS
    # ==========================================================
    st.header("4️⃣ Extreme Weather Events")

    high_temp = filtered_df[
        filtered_df["temperature_celsius"] >
        filtered_df["temperature_celsius"].quantile(0.95)
    ]

    heavy_rain = filtered_df[
        filtered_df["precip_mm"] >
        filtered_df["precip_mm"].quantile(0.95)
    ]

    st.write("🔥 High Temperature Events:", len(high_temp))
    st.write("🌧 Heavy Rain Events:", len(heavy_rain))

    # ==========================================================
    # 5️⃣ REGIONAL COMPARISON
    # ==========================================================
    st.header("5️⃣ Regional Comparison")

    country_comparison = (
        df.groupby("country")["temperature_celsius"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig3, ax3 = plt.subplots()
    country_comparison.plot(kind="bar", ax=ax3)
    ax3.set_ylabel("Average Temperature")
    st.pyplot(fig3)

    # ==========================================================
    # 6️⃣ DASHBOARD DESIGN LAYOUT EXPLANATION
    # ==========================================================
    st.header("6️⃣ Dashboard Design Structure")

    st.write("""
    The dashboard is structured into clear analytical sections:
    - Statistical Summary for distribution analysis
    - Correlation Heatmap for relationship analysis
    - Seasonal Trend Charts for pattern identification
    - Extreme Event Detection for anomaly analysis
    - Regional Comparison for cross-country evaluation
    """)

    st.success("Milestone 2 Requirements Successfully Implemented ✅")