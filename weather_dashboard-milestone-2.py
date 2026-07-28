import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Global Weather Dashboard", layout="wide")

st.title("🌍 Global Weather Analysis Dashboard")
#st.markdown("Milestone 2 - Core Analysis & Visualization")

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("C:/Users/Hi/Downloads/preprocessed_weather_dataset (2).csv")

# Convert date column
if "last_updated" in df.columns:
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df["month"] = df["last_updated"].dt.month

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

if "country" in df.columns:
    country = st.sidebar.selectbox("Select Country", df["country"].unique())
    df = df[df["country"] == country]

# ----------------------------
# KPI Section
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Temperature (°C)", round(df["temperature_celsius"].mean(),2))
col2.metric("Max Temperature (°C)", round(df["temperature_celsius"].max(),2))
col3.metric("Min Temperature (°C)", round(df["temperature_celsius"].min(),2))

# Extreme Events (Top 5%)
threshold = df["temperature_celsius"].quantile(0.95)
extreme_count = df[df["temperature_celsius"] > threshold].shape[0]
col4.metric("Extreme Heat Events", extreme_count)

# ----------------------------
# Monthly Trend Line Chart
# ----------------------------
if "month" in df.columns:
    monthly_avg = df.groupby("month")["temperature_celsius"].mean().reset_index()
    fig_line = px.line(monthly_avg, x="month", y="temperature_celsius",
                       title="Monthly Average Temperature Trend")
    st.plotly_chart(fig_line, use_container_width=True)

# ----------------------------
# Regional Comparison Bar Chart
# ----------------------------
if "country" in df.columns:
    region_avg = df.groupby("country")["temperature_celsius"].mean().reset_index()
    fig_bar = px.bar(region_avg.sort_values("temperature_celsius", ascending=False),
                     x="country", y="temperature_celsius",
                     title="Regional Comparison Average Temperature by Country")
    st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------
# Correlation Heatmap
# ----------------------------
numeric_df = df.select_dtypes(include=np.number)
corr = numeric_df.corr()

fig_heatmap = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
st.plotly_chart(fig_heatmap, use_container_width=True)

# ----------------------------
# Scatter Plot (Extreme Detection)
# ----------------------------
fig_scatter = px.scatter(df,
                         x="temperature_celsius",
                         y="humidity",
                         size="wind_kph",
                         color="temperature_celsius",
                         title="Temperature vs Humidity (Extreme Pattern)")
st.plotly_chart(fig_scatter, use_container_width=True)
