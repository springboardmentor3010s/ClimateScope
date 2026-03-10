import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Regional Comparison", layout="wide")

st.title("🌍 Regional Comparison")

# ------------------------------------------------
# Load Dataset
# ------------------------------------------------

df = pd.read_csv("D:/climateScope/data/processed/cleaned_global__weather.csv")

df["last_updated"] = pd.to_datetime(df["last_updated"])
df["year"] = df["last_updated"].dt.year

# ------------------------------------------------
# Country Selection
# ------------------------------------------------

countries = sorted(df["country"].unique())

colA, colB = st.columns(2)

countryA = colA.selectbox("Select Country A", countries)
countryB = colB.selectbox("Select Country B", countries)

dataA = df[df["country"] == countryA]
dataB = df[df["country"] == countryB]

# ------------------------------------------------
# KPI Calculations
# ------------------------------------------------

avg_temp_A = dataA["temperature_celsius"].mean()
avg_temp_B = dataB["temperature_celsius"].mean()

temp_diff = avg_temp_A - avg_temp_B

rain_diff = dataA["precip_mm"].mean() - dataB["precip_mm"].mean()

wind_diff = dataA["wind_kph"].mean() - dataB["wind_kph"].mean()

# ------------------------------------------------
# KPI Display
# ------------------------------------------------

st.subheader("📊 Regional Comparison KPIs")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(f"{countryA} Avg Temp", f"{avg_temp_A:.2f} °C")
k2.metric(f"{countryB} Avg Temp", f"{avg_temp_B:.2f} °C")
k3.metric("Temp Difference", f"{temp_diff:.2f} °C")
k4.metric("Rainfall Difference", f"{rain_diff:.2f} mm")
k5.metric("Wind Difference", f"{wind_diff:.2f} kph")

st.divider()

# ------------------------------------------------
# Dual Line Comparison
# ------------------------------------------------

st.subheader("📈 Temperature Trend Comparison")

compare_df = df[df["country"].isin([countryA, countryB])]

trend = (
    compare_df.groupby(["year", "country"])["temperature_celsius"]
    .mean()
    .reset_index()
)

fig_line = px.line(
    trend,
    x="year",
    y="temperature_celsius",
    color="country",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)

# ------------------------------------------------
# Bar Comparison
# ------------------------------------------------

st.subheader("📊 Weather Metrics Comparison")

metrics = pd.DataFrame({
    "Metric": ["Temperature", "Rainfall", "Wind"],
    countryA: [
        dataA["temperature_celsius"].mean(),
        dataA["precip_mm"].mean(),
        dataA["wind_kph"].mean()
    ],
    countryB: [
        dataB["temperature_celsius"].mean(),
        dataB["precip_mm"].mean(),
        dataB["wind_kph"].mean()
    ]
})

fig_bar = px.bar(
    metrics,
    x="Metric",
    y=[countryA, countryB],
    barmode="group"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ------------------------------------------------
# Radar Chart (Advanced)
# ------------------------------------------------

st.subheader("🕸 Radar Chart Comparison")

categories = ["Temperature", "Rainfall", "Wind"]

values_A = [
    dataA["temperature_celsius"].mean(),
    dataA["precip_mm"].mean(),
    dataA["wind_kph"].mean()
]

values_B = [
    dataB["temperature_celsius"].mean(),
    dataB["precip_mm"].mean(),
    dataB["wind_kph"].mean()
]

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=values_A,
    theta=categories,
    fill='toself',
    name=countryA
))

fig_radar.add_trace(go.Scatterpolar(
    r=values_B,
    theta=categories,
    fill='toself',
    name=countryB
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True
)

st.plotly_chart(fig_radar, use_container_width=True)

# ------------------------------------------------
# Regional Ranking
# ------------------------------------------------

st.subheader("🏆 Regional Temperature Ranking")

ranking = (
    df.groupby("country")["temperature_celsius"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_rank = px.bar(
    ranking,
    x="country",
    y="temperature_celsius",
    color="temperature_celsius",
    color_continuous_scale="OrRd"
)

st.plotly_chart(fig_rank, use_container_width=True)