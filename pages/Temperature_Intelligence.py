import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Temperature Intelligence", layout="wide")

st.title("🌡 Temperature Intelligence")

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

df = pd.read_csv("D:/climateScope/data/processed/cleaned_global__weather.csv")

df["last_updated"] = pd.to_datetime(df["last_updated"])
df["year"] = df["last_updated"].dt.year
df["month"] = df["last_updated"].dt.month

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------

st.sidebar.header("Temperature Filters")

country_list = sorted(df["country"].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    country_list,
    default=country_list[:3]
)

filtered_df = df[df["country"].isin(selected_countries)]

# ---------------------------------------------------
# KPI Calculations
# ---------------------------------------------------

current_avg = filtered_df["temperature_celsius"].mean()
max_temp = filtered_df["temperature_celsius"].max()
min_temp = filtered_df["temperature_celsius"].min()

# anomaly = difference from long-term mean
global_avg = df["temperature_celsius"].mean()
temp_anomaly = current_avg - global_avg

# 5-year trend
yearly_avg = filtered_df.groupby("year")["temperature_celsius"].mean().reset_index()

last_5 = yearly_avg.tail(5)

if len(last_5) > 1:
    trend_percent = (
        (last_5.iloc[-1]["temperature_celsius"] -
         last_5.iloc[0]["temperature_celsius"])
        / last_5.iloc[0]["temperature_celsius"]
    ) * 100
else:
    trend_percent = 0

# trend arrow
trend_arrow = "▲" if trend_percent > 0 else "▼"

# anomaly color
anomaly_color = "red" if temp_anomaly > 0 else "blue"

# ---------------------------------------------------
# KPI Display
# ---------------------------------------------------

st.subheader("📊 Temperature KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Current Avg Temp", f"{current_avg:.2f} °C")
col2.metric("Max Temperature", f"{max_temp:.2f} °C")
col3.metric("Min Temperature", f"{min_temp:.2f} °C")

col4.markdown(
    f"**Temperature Anomaly:** <span style='color:{anomaly_color}; font-size:20px;'> {temp_anomaly:.2f} °C</span>",
    unsafe_allow_html=True
)

col5.metric("5-Year Trend %", f"{trend_percent:.2f}% {trend_arrow}")

st.divider()

# ---------------------------------------------------
# Time Series Trend (Yearly)
# ---------------------------------------------------

st.subheader("📈 Yearly Temperature Trend")

fig_year = px.line(
    yearly_avg,
    x="year",
    y="temperature_celsius",
    markers=True,
    color_discrete_sequence=["orange"]
)

st.plotly_chart(fig_year, use_container_width=True)

# ---------------------------------------------------
# Monthly Trend
# ---------------------------------------------------

st.subheader("📅 Monthly Temperature Trend")

monthly_avg = (
    filtered_df.groupby("month")["temperature_celsius"]
    .mean()
    .reset_index()
)

fig_month = px.line(
    monthly_avg,
    x="month",
    y="temperature_celsius",
    markers=True,
    color_discrete_sequence=["red"]
)

st.plotly_chart(fig_month, use_container_width=True)

# ---------------------------------------------------
# Seasonal Heatmap
# ---------------------------------------------------

st.subheader("🌡 Seasonal Temperature Heatmap")

pivot = filtered_df.pivot_table(
    values="temperature_celsius",
    index="month",
    columns="year",
    aggfunc="mean"
)

fig_heatmap = px.imshow(
    pivot,
    aspect="auto",
    color_continuous_scale="RdBu_r"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# ---------------------------------------------------
# Temperature Distribution
# ---------------------------------------------------

st.subheader("📊 Temperature Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="temperature_celsius",
    nbins=50,
    color_discrete_sequence=["orange"]
)

st.plotly_chart(fig_hist, use_container_width=True)

# ---------------------------------------------------
# Multi-Country Comparison
# ---------------------------------------------------

st.subheader("🌍 Multi-Country Temperature Comparison")

compare_data = (
    filtered_df.groupby(["year","country"])["temperature_celsius"]
    .mean()
    .reset_index()
)

fig_compare = px.line(
    compare_data,
    x="year",
    y="temperature_celsius",
    color="country",
    markers=True
)

st.plotly_chart(fig_compare, use_container_width=True)