import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚠ Climate Risk Intelligence")

st.write("This page estimates climate risk using multiple environmental indicators.")

df = pd.read_csv("/Users/garikapatiaishwarya/Desktop/climatescope/data/processed/global_weather_cleaned_daily.csv")

# Risk Score
df["risk_score"] = (
    df["temperature_celsius"]*0.5 +
    df["wind_kph"]*0.3 +
    df["precip_mm"]*0.2
)

risk_mean = df["risk_score"].mean()

# Volatility
volatility = df["risk_score"].std()

# Trend
trend = df.groupby("year")["risk_score"].mean()

trend_dir = "▲ Increasing" if trend.iloc[-1] > trend.iloc[0] else "▼ Decreasing"

# Category

if risk_mean < 30:
    category="Low"
elif risk_mean < 60:
    category="Moderate"
else:
    category="High"

# KPIs
c1,c2,c3,c4 = st.columns(4)

c1.metric("Climate Risk Score", round(risk_mean,2))
c2.metric("Risk Category", category)
c3.metric("Volatility Index", round(volatility,2))
c4.metric("Trend Direction", trend_dir)

# Risk by Country
st.subheader("Risk Score by Country")

risk_country = df.groupby("country")["risk_score"].mean().reset_index()

fig = px.bar(risk_country, x="country", y="risk_score")

st.plotly_chart(fig, use_container_width=True)

st.info("Insight: Countries with higher risk scores experience stronger climate stress.")

# Risk Trend

st.subheader("Risk Trend Over Time")

trend_df = trend.reset_index()

fig2 = px.line(trend_df, x="year", y="risk_score")

st.plotly_chart(fig2, use_container_width=True)

st.info("Insight: Increasing risk trends highlight worsening climate conditions.")

# Risk Heatmap

st.subheader("Risk Heatmap")

heat = df.pivot_table(
    values="risk_score",
    index="year",
    columns="month"
)

fig3 = px.imshow(heat)

st.plotly_chart(fig3, use_container_width=True)

st.info("Insight: The heatmap highlights periods of elevated climate risk.")

# Top Risk Countries

st.subheader("Top 10 Risk Countries")

top = risk_country.nlargest(10,"risk_score")

fig4 = px.bar(top, x="country", y="risk_score")

st.plotly_chart(fig4, use_container_width=True)

st.info("Insight: These countries require stronger climate adaptation strategies.")