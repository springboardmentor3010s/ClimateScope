import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌧 Precipitation & Wind Intelligence")

df = pd.read_csv("/Users/garikapatiaishwarya/Desktop/climatescope/data/processed/global_weather_cleaned_daily.csv")

total_rain = df["precip_mm"].sum()
heavy_rain = df[df["precip_mm"] > 50].shape[0]
avg_wind = df["wind_kph"].mean()
high_wind = df[df["wind_kph"] > 60].shape[0]

c1,c2,c3,c4 = st.columns(4)

c1.metric("Total Rainfall", round(total_rain,2))
c2.metric("Heavy Rain Days", heavy_rain)
c3.metric("Avg Wind Speed", round(avg_wind,2))
c4.metric("High Wind Events", high_wind)

# Rainfall Trend
rain = df.groupby("year")["precip_mm"].mean().reset_index()

fig = px.line(rain, x="year", y="precip_mm")

st.plotly_chart(fig, use_container_width=True)

st.info("Insight: Rainfall trends highlight how precipitation changes across years.")

# Wind Trend
wind = df.groupby("year")["wind_kph"].mean().reset_index()

fig2 = px.line(wind, x="year", y="wind_kph")

st.plotly_chart(fig2, use_container_width=True)

st.info("Insight: Increasing wind trends may indicate stronger atmospheric disturbances.")

# Scatter
scatter = px.scatter(df, x="precip_mm", y="wind_kph")

st.plotly_chart(scatter, use_container_width=True)

st.info("Insight: This chart reveals the relationship between rainfall intensity and wind speed.")

# Ranking
rank = df.groupby("country")["precip_mm"].mean().nlargest(10).reset_index()

fig3 = px.bar(rank, x="country", y="precip_mm")

st.plotly_chart(fig3, use_container_width=True)

st.info("Insight: Some countries consistently receive significantly higher rainfall.")