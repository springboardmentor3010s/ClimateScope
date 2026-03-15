import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.load_data import load_data

st.title("🌍 Regional Climate Comparison")

df = load_data()

# Bar Chart
st.subheader("Average Temperature by Country")

avg_temp = df.groupby("country")["temperature_celsius"].mean().reset_index()

fig_bar = px.bar(
    avg_temp,
    x="country",
    y="temperature_celsius",
    title="Average Temperature Comparison"
)

st.plotly_chart(fig_bar)

# Radar Chart
st.subheader("Climate Indicator Comparison")

categories = ["temperature_celsius","precip_mm","wind_kph","humidity"]

avg = df.groupby("country")[categories].mean().reset_index()

fig = go.Figure()

for i in range(len(avg)):
    fig.add_trace(go.Scatterpolar(
        r=avg.loc[i,categories],
        theta=categories,
        fill='toself',
        name=avg.loc[i,"country"]
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    title="Climate Radar Comparison"
)

st.plotly_chart(fig)

# Line Comparison
st.subheader("Temperature Trend Comparison")
top_countries = df.groupby("country")["temperature_celsius"].mean().nlargest(10).index

filtered = df[df["country"].isin(top_countries)]

fig = px.line(
    filtered,
    x="month",
    y="temperature_celsius",
    color="country",
    title="Temperature Trend for Top 10 Hottest Countries"
)

st.plotly_chart(fig, use_container_width=True)
# avg_temp = df.groupby("month")["temperature_celsius"].mean().reset_index()

# fig = px.line(
#     avg_temp,
#     x="month",
#     y="temperature_celsius",
#     title="Global Average Temperature Trend",
#     markers=True
# )

# st.plotly_chart(fig, use_container_width=True)