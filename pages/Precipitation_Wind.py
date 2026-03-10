import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Precipitation & Wind Intelligence", layout="wide")

st.title("🌧 Precipitation & Wind Intelligence")

# ------------------------------------------------
# Load Dataset
# ------------------------------------------------

df = pd.read_csv("D:/climateScope/data/processed/cleaned_global__weather.csv")
 
df["last_updated"] = pd.to_datetime(df["last_updated"])
df["year"] = df["last_updated"].dt.year
df["month"] = df["last_updated"].dt.month

# ------------------------------------------------
# Sidebar Filters
# ------------------------------------------------

st.sidebar.header("🌍 Regional Filters")

country_list = sorted(df["country"].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    country_list,
    default=country_list[:3]
)

filtered_df = df[df["country"].isin(selected_countries)]

# ------------------------------------------------
# KPI Calculations
# ------------------------------------------------

total_rainfall = filtered_df["precip_mm"].sum()

heavy_rain_days = filtered_df[filtered_df["precip_mm"] > 50].shape[0]

avg_wind_speed = filtered_df["wind_kph"].mean()

high_wind_events = filtered_df[filtered_df["wind_kph"] > 60].shape[0]

# Rainfall variability index (coefficient of variation)
rain_variability = (
    filtered_df["precip_mm"].std() /
    filtered_df["precip_mm"].mean()
) * 100

# ------------------------------------------------
# KPI Display
# ------------------------------------------------

st.subheader("📊 Rainfall & Wind KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🌧 Total Rainfall", f"{total_rainfall:.0f} mm")
col2.metric("🌧 Heavy Rain Days", heavy_rain_days)
col3.metric("💨 Avg Wind Speed", f"{avg_wind_speed:.2f} kph")
col4.metric("🌪 High Wind Events", high_wind_events)
col5.metric("📊 Rainfall Variability", f"{rain_variability:.2f}%")

st.divider()

# ------------------------------------------------
# Rainfall Trend
# ------------------------------------------------

st.subheader("🌧 Rainfall Trend")

rain_trend = (
    filtered_df.groupby("year")["precip_mm"]
    .sum()
    .reset_index()
)

fig_rain = px.line(
    rain_trend,
    x="year",
    y="precip_mm",
    markers=True,
    color_discrete_sequence=["blue"]
)

st.plotly_chart(fig_rain, use_container_width=True)

# ------------------------------------------------
# Wind Speed Trend
# ------------------------------------------------

st.subheader("💨 Wind Speed Trend")

wind_trend = (
    filtered_df.groupby("year")["wind_kph"]
    .mean()
    .reset_index()
)

fig_wind = px.line(
    wind_trend,
    x="year",
    y="wind_kph",
    markers=True,
    color_discrete_sequence=["orange"]
)

st.plotly_chart(fig_wind, use_container_width=True)

# ------------------------------------------------
# Rain vs Wind Scatter Plot
# ------------------------------------------------

st.subheader("🌧💨 Rain vs Wind Relationship")

fig_scatter = px.scatter(
    filtered_df,
    x="precip_mm",
    y="wind_kph",
    color="country",
    size="wind_kph",
    opacity=0.6
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ------------------------------------------------
# Country Ranking
# ------------------------------------------------

st.subheader("🌍 Country Rainfall Ranking")

country_rank = (
    filtered_df.groupby("country")["precip_mm"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_bar = px.bar(
    country_rank,
    x="country",
    y="precip_mm",
    color="precip_mm",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_bar, use_container_width=True)