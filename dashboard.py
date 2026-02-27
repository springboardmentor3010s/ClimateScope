import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/cleaned_weather_monthly.csv")

st.set_page_config(layout="wide")
st.title("🌍 ClimateScope - Global Climate Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

selected_country = st.sidebar.selectbox(
    "Select Country",
    df['country'].unique()
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df['year'].unique())
)

selected_metric = st.sidebar.selectbox(
    "Select Metric",
    ["temperature_celsius", "precip_mm", "wind_kph", "humidity"]
)

filtered_df = df[
    (df['country'] == selected_country) &
    (df['year'] == selected_year)
]

# 🌍 Global Map
st.subheader("Global Temperature Distribution")

fig_map = px.choropleth(
    df[df['year'] == selected_year],
    locations="country",
    locationmode="country names",
    color=selected_metric,
    title="Global Distribution"
)

st.plotly_chart(fig_map, use_container_width=True)

# 📈 Monthly Trend
st.subheader("Monthly Trend")

fig_line = px.line(
    filtered_df,
    x="month",
    y=selected_metric,
    title=f"{selected_metric} Trend - {selected_country}"
)

st.plotly_chart(fig_line, use_container_width=True)

# 📊 Correlation Heatmap
st.subheader("Correlation Heatmap")

corr = df[['temperature_celsius','humidity','wind_kph','precip_mm','pressure_mb']].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)