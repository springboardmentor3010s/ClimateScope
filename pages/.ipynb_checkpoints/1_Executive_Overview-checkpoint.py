import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("GlobalWeather_Preprocessed.csv")

st.title("📊 Executive Overview")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Avg Temp", round(df["temperature_celsius"].mean(), 2))
col2.metric("Avg Humidity", round(df["humidity"].mean(), 2))
col3.metric("Avg Wind", round(df["wind_kph"].mean(), 2))

# Map
st.subheader("🌍 Global Temperature Map")
fig_map = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="temperature_celsius",
    zoom=1
)
fig_map.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig_map, use_container_width=True)

# Trend
st.subheader("📈 Temperature Distribution")
fig = px.histogram(df, x="temperature_celsius")
st.plotly_chart(fig, use_container_width=True)

# Top Countries
top = df.groupby("country")["temperature_celsius"].mean().nlargest(5).reset_index()
fig2 = px.bar(top, x="country", y="temperature_celsius")
st.plotly_chart(fig2, use_container_width=True)