import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌍 Regional Climate Comparison")

st.write("Compare climate indicators across countries to understand regional differences.")

df = pd.read_csv("/Users/garikapatiaishwarya/Desktop/climatescope/data/processed/global_weather_cleaned_daily.csv")

countries = sorted(df["country"].unique())

col1,col2 = st.columns(2)

countryA = col1.selectbox("Country A", countries)
countryB = col2.selectbox("Country B", countries)

dataA = df[df["country"]==countryA]
dataB = df[df["country"]==countryB]

# KPIs

c1,c2,c3 = st.columns(3)

c1.metric("Country A Avg Temp", round(dataA["temperature_celsius"].mean(),2))
c2.metric("Country B Avg Temp", round(dataB["temperature_celsius"].mean(),2))

temp_diff = dataA["temperature_celsius"].mean() - dataB["temperature_celsius"].mean()

c3.metric("Temp Difference", round(temp_diff,2))

# Rainfall Difference
rain_diff = dataA["precip_mm"].mean() - dataB["precip_mm"].mean()

# Wind Difference
wind_diff = dataA["wind_kph"].mean() - dataB["wind_kph"].mean()

st.write("Rainfall Difference:", round(rain_diff,2))
st.write("Wind Difference:", round(wind_diff,2))

# Dual Line Comparison

st.subheader("Temperature Trend Comparison")

comp = df[df["country"].isin([countryA,countryB])]

fig = px.line(comp, x="year", y="temperature_celsius", color="country")

st.plotly_chart(fig, use_container_width=True)

st.info("Insight: This chart shows how temperature trends differ between two regions.")

# Bar Comparison

st.subheader("Rainfall Comparison")

bar_data = pd.DataFrame({
    "Country":[countryA,countryB],
    "Rainfall":[dataA["precip_mm"].mean(),dataB["precip_mm"].mean()]
})

fig2 = px.bar(bar_data, x="Country", y="Rainfall")

st.plotly_chart(fig2, use_container_width=True)

st.info("Insight: Rainfall differences can influence agriculture and ecosystem stability.")

# Radar Chart

st.subheader("Climate Indicator Radar")

radar_data = pd.DataFrame({
    "Metric":["Temperature","Rainfall","Wind"],
    countryA:[
        dataA["temperature_celsius"].mean(),
        dataA["precip_mm"].mean(),
        dataA["wind_kph"].mean()
    ],
    countryB:[
        dataB["temperature_celsius"].mean(),
        dataB["precip_mm"].mean(),
        dataB["wind_kph"].mean()
    ]
})

fig3 = px.line_polar(
    radar_data,
    r=countryA,
    theta="Metric",
    line_close=True
)

st.plotly_chart(fig3, use_container_width=True)

st.info("Insight: Radar visualization highlights overall climate profile differences.")