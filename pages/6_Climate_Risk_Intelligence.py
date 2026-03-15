import streamlit as st
import plotly.express as px
from utils.load_data import load_data

st.title("⚠ Climate Risk Intelligence")

df = load_data()

# Risk score calculation
df["risk_score"] = (
    df["temperature_celsius"]*0.4 +
    df["precip_mm"]*0.3 +
    df["wind_kph"]*0.3
)

risk = df.groupby("country")["risk_score"].mean().reset_index()

# Bar Chart
fig_bar = px.bar(
    risk.sort_values("risk_score",ascending=False),
    x="country",
    y="risk_score",
    color="risk_score",
    title="Climate Risk Score by Country"
)

st.plotly_chart(fig_bar)

# Pie Chart
fig_pie = px.pie(
    risk,
    names="country",
    values="risk_score",
    title="Risk Distribution"
)

st.plotly_chart(fig_pie)

# Scatter Chart
fig_scatter = px.scatter(
    df,
    x="temperature_celsius",
    y="precip_mm",
    color="risk_score",
    size="wind_kph",
    title="Climate Risk Pattern"
)

st.plotly_chart(fig_scatter)