import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("GlobalWeather_Preprocessed.csv")

st.title("🌡 Temperature Intelligence")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Max Temp", df["temperature_celsius"].max())
col2.metric("Min Temp", df["temperature_celsius"].min())
col3.metric("Avg Temp", round(df["temperature_celsius"].mean(), 2))

# Histogram
st.subheader("Temperature Distribution")
fig = px.histogram(df, x="temperature_celsius", nbins=30)
st.plotly_chart(fig)

# Heatmap
st.subheader("Correlation Heatmap")
corr = df[["temperature_celsius", "humidity", "wind_kph"]].corr()
fig2 = px.imshow(corr, text_auto=True)
st.plotly_chart(fig2)