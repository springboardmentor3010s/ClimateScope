import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Extreme Events Monitor", layout="wide")

st.title("🚨 Extreme Events Monitor")

# ------------------------------------------------
# Load Dataset
# ------------------------------------------------

df = pd.read_csv("D:/climateScope/data/processed/cleaned_global__weather.csv")

df["last_updated"] = pd.to_datetime(df["last_updated"])
df["year"] = df["last_updated"].dt.year
df["month"] = df["last_updated"].dt.month

# ------------------------------------------------
# Define Extreme Event Thresholds
# ------------------------------------------------

heatwave = df[df["temperature_celsius"] > 40]
heavy_rain = df[df["precip_mm"] > 100]
high_wind = df[df["wind_kph"] > 60]

# label event type
df["event_type"] = "Normal"

df.loc[df["temperature_celsius"] > 40, "event_type"] = "Heatwave"
df.loc[df["precip_mm"] > 100, "event_type"] = "Heavy Rain"
df.loc[df["wind_kph"] > 60, "event_type"] = "High Wind"

extreme_events = df[df["event_type"] != "Normal"]

# ------------------------------------------------
# KPI Calculations
# ------------------------------------------------

total_extreme = extreme_events.shape[0]

heatwave_days = heatwave.shape[0]

heavy_rain_events = heavy_rain.shape[0]

high_wind_events = high_wind.shape[0]

highest_risk_country = (
    extreme_events.groupby("country")
    .size()
    .idxmax()
)

# ------------------------------------------------
# Risk Level Indicator
# ------------------------------------------------

if total_extreme < 100:
    risk_level = "🟢 Low"
elif total_extreme < 500:
    risk_level = "🟡 Medium"
else:
    risk_level = "🔴 High"

# ------------------------------------------------
# KPI Layout
# ------------------------------------------------

st.subheader("📊 Extreme Event KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🚨 Total Extreme Events", total_extreme)
col2.metric("🔥 Heatwave Days", heatwave_days)
col3.metric("🌧 Heavy Rain Events", heavy_rain_events)
col4.metric("🌪 High Wind Events", high_wind_events)
col5.metric("⚠ Highest Risk Country", highest_risk_country)

st.success(f"Risk Level Indicator: {risk_level}")

st.divider()

# ------------------------------------------------
# Extreme Event Timeline
# ------------------------------------------------

st.subheader("📈 Extreme Event Timeline")

timeline = (
    extreme_events.groupby("year")
    .size()
    .reset_index(name="events")
)

fig_timeline = px.line(
    timeline,
    x="year",
    y="events",
    markers=True
)

st.plotly_chart(fig_timeline, use_container_width=True)

# ------------------------------------------------
# Country-wise Event Map
# ------------------------------------------------

st.subheader("🌍 Country-wise Extreme Event Map")

country_events = (
    extreme_events.groupby("country")
    .size()
    .reset_index(name="events")
)

fig_map = px.choropleth(
    country_events,
    locations="country",
    locationmode="country names",
    color="events",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_map, use_container_width=True)

# ------------------------------------------------
# Monthly Extreme Heatmap
# ------------------------------------------------

st.subheader("🔥 Monthly Extreme Event Heatmap")

heatmap_data = extreme_events.pivot_table(
    values="temperature_celsius",
    index="month",
    columns="year",
    aggfunc="count"
)

fig_heatmap = px.imshow(
    heatmap_data,
    color_continuous_scale="Reds",
    aspect="auto"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# ------------------------------------------------
# Event Distribution
# ------------------------------------------------

st.subheader("📊 Event Distribution by Type")

fig_pie = px.pie(
    extreme_events,
    names="event_type"
)

st.plotly_chart(fig_pie, use_container_width=True)

# Optional bar version

fig_bar = px.bar(
    extreme_events.groupby("event_type")
    .size()
    .reset_index(name="count"),
    x="event_type",
    y="count",
    color="event_type"
)

st.plotly_chart(fig_bar, use_container_width=True)