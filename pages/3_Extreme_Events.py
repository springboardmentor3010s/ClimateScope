import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("GlobalWeather_Preprocessed.csv")

st.title("⚠ Extreme Events Monitor")

# Filter extreme
extreme = df[
    (df["temperature_celsius"] > 40) |
    (df["wind_kph"] > 60)
]

# KPI
st.metric("Extreme Events Count", extreme.shape[0])

# Table
st.dataframe(extreme)

# Chart
st.subheader("Extreme Temperature Locations")
fig = px.bar(extreme, x="location_name", y="temperature_celsius")
st.plotly_chart(fig)