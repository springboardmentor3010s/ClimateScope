import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Climate Risk Intelligence", layout="wide")

st.title("⚠ Climate Risk Intelligence")

# ------------------------------------------------
# Load Dataset
# ------------------------------------------------

df = pd.read_csv("D:/climateScope/data/processed/cleaned_global__weather.csv")

df["last_updated"] = pd.to_datetime(df["last_updated"])
df["year"] = df["last_updated"].dt.year
df["month"] = df["last_updated"].dt.month

# ------------------------------------------------
# Climate Risk Score Calculation
# ------------------------------------------------

df["risk_score"] = (
    (df["temperature_celsius"] * 0.4) +
    (df["precip_mm"] * 0.3) +
    (df["wind_kph"] * 0.3)
)

# ------------------------------------------------
# KPI Calculations
# ------------------------------------------------

climate_risk_score = df["risk_score"].mean()

volatility_index = df["risk_score"].std()

# risk category
if climate_risk_score < 20:
    risk_category = "🟢 Low"
elif climate_risk_score < 40:
    risk_category = "🟡 Medium"
else:
    risk_category = "🔴 High"

# trend direction
yearly_risk = (
    df.groupby("year")["risk_score"]
    .mean()
    .reset_index()
)

trend_direction = "▲ Increasing" if yearly_risk.iloc[-1]["risk_score"] > yearly_risk.iloc[0]["risk_score"] else "▼ Decreasing"

# ------------------------------------------------
# KPI Display
# ------------------------------------------------

st.subheader("📊 Climate Risk KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Climate Risk Score", f"{climate_risk_score:.2f}")
col2.metric("Risk Category", risk_category)
col3.metric("Volatility Index", f"{volatility_index:.2f}")
col4.metric("Trend Direction", trend_direction)

st.divider()

# ------------------------------------------------
# Risk Score by Country
# ------------------------------------------------

st.subheader("🌍 Risk Score by Country")

country_risk = (
    df.groupby("country")["risk_score"]
    .mean()
    .reset_index()
)

fig_map = px.choropleth(
    country_risk,
    locations="country",
    locationmode="country names",
    color="risk_score",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_map, use_container_width=True)

# ------------------------------------------------
# Risk Trend Over Time
# ------------------------------------------------

st.subheader("📈 Climate Risk Trend")

fig_trend = px.line(
    yearly_risk,
    x="year",
    y="risk_score",
    markers=True,
    color_discrete_sequence=["red"]
)

st.plotly_chart(fig_trend, use_container_width=True)

# ------------------------------------------------
# Risk Heatmap
# ------------------------------------------------

st.subheader("🔥 Risk Heatmap (Month vs Year)")

heatmap_data = df.pivot_table(
    values="risk_score",
    index="month",
    columns="year",
    aggfunc="mean"
)

fig_heatmap = px.imshow(
    heatmap_data,
    aspect="auto",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# ------------------------------------------------
# Top 10 Risk Countries
# ------------------------------------------------

st.subheader("🏆 Top 10 High Risk Countries")

top_risk = (
    df.groupby("country")["risk_score"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_bar = px.bar(
    top_risk,
    x="country",
    y="risk_score",
    color="risk_score",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_bar, use_container_width=True)