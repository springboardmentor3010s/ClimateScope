import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("🌍 ClimateScope Interactive Dashboard")



df = pd.read_csv("D:\climateScope\data\processed\_cleaned_global__weather.csv")

df['last_updated'] = pd.to_datetime(df['last_updated'])
df['year'] = df['last_updated'].dt.year
df['month'] = df['last_updated'].dt.month


st.sidebar.header("Filters")

selected_country = st.sidebar.selectbox(
    "Select Country",
    sorted(df['country'].unique())
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df['year'].unique())
)

filtered_df = df[
    (df['country'] == selected_country) &
    (df['year'] == selected_year)
]

st.subheader("Global Temperature Distribution")

country_temp = (
    df.groupby("country")["temperature_celsius"]
    .mean()
    .reset_index()
)

fig_map = px.choropleth(
    country_temp,
    locations="country",
    locationmode="country names",
    color="temperature_celsius",
    hover_name="country",
    color_continuous_scale="RdYlBu_r"
)

st.plotly_chart(fig_map, use_container_width=True)


st.subheader(f"Monthly Temperature Trend - {selected_country} ({selected_year})")

monthly_trend = (
    filtered_df.groupby("month")["temperature_celsius"]
    .mean()
    .reset_index()
)

fig_line = px.line(
    monthly_trend,
    x="month",
    y="temperature_celsius",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)


st.subheader("Temperature vs Humidity")

fig_scatter = px.scatter(
    df,
    x="temperature_celsius",
    y="humidity",
    color="country",
    hover_data=["precip_mm", "wind_kph"]
)

st.plotly_chart(fig_scatter, use_container_width=True)


st.subheader("Seasonal Temperature Heatmap")

pivot_temp = df.pivot_table(
    values="temperature_celsius",
    index="month",
    columns="country",
    aggfunc="mean"
)

fig_heatmap = px.imshow(
    pivot_temp,
    aspect="auto",
    color_continuous_scale="RdYlBu_r"
)

st.plotly_chart(fig_heatmap, use_container_width=True)



st.subheader("Extreme Weather Event Ranking")

extreme_df = df[
    (df['temperature_celsius'] > 45) |
    (df['precip_mm'] > 200) |
    (df['wind_kph'] > 80)
]

extreme_rank = (
    extreme_df.groupby("country")
    .size()
    .reset_index(name="Extreme Event Count")
    .sort_values(by="Extreme Event Count", ascending=False)
)

fig_bar = px.bar(
    extreme_rank.head(10),
    x="Extreme Event Count",
    y="country",
    orientation="h"
)

st.plotly_chart(fig_bar, use_container_width=True)


st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_weather_data.csv",
    mime="text/csv"
)