import streamlit as st
import plotly.express as px
from utils.load_data import load_data

# ---------------- PAGE TITLE ----------------
st.title("🌡 Temperature Intelligence Dashboard")

# ---------------- LOAD DATA ----------------
df = load_data()

st.markdown(
"""
This section analyzes **temperature behavior across countries and seasons**.
It highlights distribution patterns, seasonal variations, and country comparisons.
"""
)

# ---------------- LINE TREND CHART ----------------
st.subheader("📈 Monthly Temperature Trends")

fig_line = px.line(
    df.sort_values("temperature_celsius", ascending=False).head(40),
    x="month",
    y="temperature_celsius",
    color="country",
    title="Temperature Trend Across Months",
    template="plotly_white"
)

st.plotly_chart(fig_line, use_container_width=True)


# ---------------- HISTOGRAM ----------------
st.subheader("📊 Temperature Distribution")

fig_hist = px.histogram(
    df,
    x="temperature_celsius",
    nbins=30,
    color="country",
    title="Temperature Distribution Histogram",
    template="plotly_white"
)

st.plotly_chart(fig_hist, use_container_width=True)


# ---------------- PIE CHART ----------------
st.subheader("🥧 Temperature Contribution by Country")

pie_data = df.groupby("country")["temperature_celsius"].mean().reset_index()

fig_pie = px.pie(
    pie_data.sort_values("temperature_celsius", ascending=False).head(35),
    names="country",
    values="temperature_celsius",
    title="Average Temperature Share by Country",
)

st.plotly_chart(fig_pie, use_container_width=True)


# ---------------- HEATMAP ----------------
st.subheader("🔥 Seasonal Temperature Heatmap")

heatmap = px.density_heatmap(
    df,
    x="month",
    y="year",
    z="temperature_celsius",
    color_continuous_scale="RdYlBu_r",
    title="Seasonal Temperature Patterns"
)

st.plotly_chart(heatmap, use_container_width=True)


# ---------------- BOX PLOT ----------------
st.subheader("📦 Temperature Distribution by Country")

fig_box = px.box(
    df,
    x="country",
    y="temperature_celsius",
    title="Country-wise Temperature Distribution",
    template="plotly_white"
)

st.plotly_chart(fig_box, use_container_width=True)


# ---------------- TOP HOTTEST COUNTRIES ----------------
st.subheader("🔥 Top 10 Hottest Countries")

top_hot = df.groupby("country")["temperature_celsius"].mean().reset_index()

fig_bar = px.bar(
    top_hot.sort_values("temperature_celsius", ascending=False).head(10),
    x="country",
    y="temperature_celsius",
    color="temperature_celsius",
    color_continuous_scale="Reds",
    title="Top 10 Countries by Average Temperature"
)

st.plotly_chart(fig_bar, use_container_width=True)


# ---------------- INSIGHTS ----------------
st.markdown(
"""
### 🔎 Key Insights

• Temperature trends vary significantly across different regions.  
• Some countries consistently record higher temperature averages.  
• Seasonal patterns indicate clear climatic cycles.  
• Distribution analysis helps detect unusual temperature spikes.
"""
)