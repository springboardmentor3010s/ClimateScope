import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌍 Executive Climate Overview")

st.write("This page summarizes global climate conditions using key indicators and high-level visual insights.")

df = pd.read_csv("/Users/garikapatiaishwarya/Desktop/climatescope/data/processed/global_weather_cleaned_daily.csv")

# ---------------- FILTERS ----------------
col1, col2 = st.columns(2)

country = col1.selectbox("Select Country", ["All"] + sorted(df["country"].unique()))
year = col2.selectbox("Select Year", ["All"] + sorted(df["year"].unique()))

filtered = df.copy()

if country != "All":
    filtered = filtered[filtered["country"] == country]

if year != "All":
    filtered = filtered[filtered["year"] == year]

# ---------------- KPIs ----------------

avg_temp = filtered["temperature_celsius"].mean()
total_rain = filtered["precip_mm"].sum()
avg_wind = filtered["wind_kph"].mean()

extreme = filtered[
    (filtered["temperature_celsius"] > 40) |
    (filtered["precip_mm"] > 100) |
    (filtered["wind_kph"] > 60)
]

# YoY Temperature Change
yearly = df.groupby("year")["temperature_celsius"].mean()

if len(yearly) > 1:
    yoy = ((yearly.iloc[-1] - yearly.iloc[-2]) / yearly.iloc[-2]) * 100
else:
    yoy = 0

hottest_country = filtered.groupby("country")["temperature_celsius"].mean().idxmax()

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric("🌡 Global Avg Temp", round(avg_temp,2))
c2.metric("📈 Temp Change YoY %", round(yoy,2))
c3.metric("🌧 Total Precipitation", round(total_rain,2))
c4.metric("💨 Avg Wind Speed", round(avg_wind,2))
c5.metric("🚨 Extreme Events", len(extreme))
c6.metric("🔥 Hottest Country", hottest_country)

# ---------------- CHOROPLETH MAP ----------------

st.subheader("Global Temperature Map")

country_avg = filtered.groupby("country")["temperature_celsius"].mean().reset_index()

fig = px.choropleth(
    country_avg,
    locations="country",
    locationmode="country names",
    color="temperature_celsius",
    title="Average Temperature by Country"
)

st.plotly_chart(fig, use_container_width=True)

st.info("Insight: Countries closer to the equator generally show higher average temperatures.")

# ---------------- TEMPERATURE TREND ----------------

st.subheader("Global Temperature Trend")

trend = filtered.groupby("year")["temperature_celsius"].mean().reset_index()

fig2 = px.line(trend, x="year", y="temperature_celsius", markers=True)

st.plotly_chart(fig2, use_container_width=True)

st.info("Insight: The long-term trend highlights how global temperatures change across years.")

# ---------------- TOP COUNTRIES ----------------

st.subheader("Top 5 Hottest Countries")

top5 = filtered.groupby("country")["temperature_celsius"].mean().nlargest(5).reset_index()

fig3 = px.bar(top5, x="country", y="temperature_celsius", color="temperature_celsius")

st.plotly_chart(fig3, use_container_width=True)

st.info("Insight: These countries experience the highest average temperatures in the selected period.")