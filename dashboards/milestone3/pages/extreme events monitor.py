import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚨 Extreme Events Monitor")

st.write("This dashboard detects climate anomalies such as heatwaves, heavy rainfall and strong winds.")

df = pd.read_csv("/Users/garikapatiaishwarya/Desktop/climatescope/data/processed/global_weather_cleaned_daily.csv")

# Extreme Conditions
heatwave = df[df["temperature_celsius"] > 40]
heavy_rain = df[df["precip_mm"] > 100]
high_wind = df[df["wind_kph"] > 60]

extreme = df[
    (df["temperature_celsius"] > 40) |
    (df["precip_mm"] > 100) |
    (df["wind_kph"] > 60)
]

# KPIs
c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Total Extreme Events", len(extreme))
c2.metric("Heatwave Days", len(heatwave))
c3.metric("Heavy Rain Events", len(heavy_rain))
c4.metric("High Wind Events", len(high_wind))

risk_country = extreme.groupby("country").size().idxmax()
c5.metric("Highest Risk Country", risk_country)

# Risk Level
events = len(extreme)

if events < 50:
    risk = "🟢 Low"
elif events < 150:
    risk = "🟡 Medium"
else:
    risk = "🔴 High"

st.metric("Global Risk Level", risk)

# Timeline
st.subheader("Extreme Event Timeline")

timeline = extreme.groupby("year").size().reset_index(name="events")

fig = px.line(timeline, x="year", y="events")

st.plotly_chart(fig, use_container_width=True)

st.info("Insight: Increasing extreme events may indicate climate instability.")

# Country Map
st.subheader("Country-wise Extreme Event Map")

country_events = extreme.groupby("country").size().reset_index(name="events")

fig2 = px.choropleth(
    country_events,
    locations="country",
    locationmode="country names",
    color="events"
)

st.plotly_chart(fig2, use_container_width=True)

st.info("Insight: Countries with frequent extreme events face higher climate risks.")

# Monthly Heatmap
st.subheader("Monthly Extreme Event Heatmap")

heat = extreme.pivot_table(
    index="year",
    columns="month",
    values="temperature_celsius",
    aggfunc="count"
)

fig3 = px.imshow(heat, aspect="auto")

st.plotly_chart(fig3, use_container_width=True)

st.info("Insight: Seasonal clustering of extreme events becomes visible here.")

# Event Distribution
st.subheader("Event Distribution by Type")

event_data = pd.DataFrame({
    "Event":["Heatwave","Heavy Rain","High Wind"],
    "Count":[len(heatwave),len(heavy_rain),len(high_wind)]
})

fig4 = px.pie(event_data, names="Event", values="Count")

st.plotly_chart(fig4, use_container_width=True)

st.info("Insight: This chart shows which type of extreme weather dominates globally.")