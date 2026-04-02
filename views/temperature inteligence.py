import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌡 Temperature Intelligence")

st.write("This section analyzes temperature patterns, seasonal trends and anomalies.")

df = pd.read_csv("/Users/garikapatiaishwarya/Desktop/untitled folder/global_weather_cleaned_daily.csv")

# KPIs
avg_temp = df["temperature_celsius"].mean()
max_temp = df["temperature_celsius"].max()
min_temp = df["temperature_celsius"].min()

baseline = df["temperature_celsius"].mean()
current = df[df["year"] == df["year"].max()]["temperature_celsius"].mean()

anomaly = current - baseline

trend = df.groupby("year")["temperature_celsius"].mean()

if len(trend) >= 5:
    five_year = ((trend.iloc[-1] - trend.iloc[-5]) / trend.iloc[-5]) * 100
else:
    five_year = 0

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Avg Temp", round(avg_temp,2))
c2.metric("Max Temp", round(max_temp,2))
c3.metric("Min Temp", round(min_temp,2))
c4.metric("Temperature Anomaly", round(anomaly,2))
c5.metric("5-Year Trend %", round(five_year,2))

# ---------------- TIME SERIES ----------------

st.subheader("Temperature Trend")

trend_df = df.groupby("year")["temperature_celsius"].mean().reset_index()

fig = px.line(trend_df, x="year", y="temperature_celsius")

st.plotly_chart(fig, use_container_width=True)

st.info("Insight: This trend illustrates long-term temperature change patterns.")

# ---------------- HEATMAP ----------------

st.subheader("Seasonal Temperature Heatmap")

heat = df.pivot_table(values="temperature_celsius", index="year", columns="month")

fig2 = px.imshow(heat, aspect="auto")

st.plotly_chart(fig2, use_container_width=True)

st.info("Insight: Seasonal patterns become visible with hotter months showing stronger intensity.")

# ---------------- HISTOGRAM ----------------

st.subheader("Temperature Distribution")

hist = px.histogram(df, x="temperature_celsius", nbins=40)

st.plotly_chart(hist, use_container_width=True)

st.info("Insight: This distribution shows how frequently temperature values occur globally.")

# ---------------- MULTI COUNTRY COMPARISON ----------------

st.subheader("Country Temperature Comparison")

countries = st.multiselect("Select Countries", df["country"].unique())

if countries:
    comp = df[df["country"].isin(countries)]

    fig3 = px.line(comp, x="year", y="temperature_celsius", color="country")

    st.plotly_chart(fig3, use_container_width=True)

    st.info("Insight: Comparing countries helps identify regional climate differences.")