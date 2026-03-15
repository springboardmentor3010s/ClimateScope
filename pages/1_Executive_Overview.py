import streamlit as st
import plotly.express as px
import pycountry
from utils.load_data import load_data


# ---------------- PAGE TITLE ----------------
st.title("🌍 Executive Climate Overview")


# ---------------- LOAD DATA ----------------
df = load_data()


# ---------------- KPI METRICS ----------------
avg_temp = df["temperature_celsius"].mean()
max_temp = df["temperature_celsius"].max()
total_rain = df["precip_mm"].sum()
avg_wind = df["wind_kph"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡 Avg Temperature", f"{avg_temp:.2f} °C")
col2.metric("🔥 Max Temperature", f"{max_temp:.2f} °C")
col3.metric("🌧 Total Rainfall", f"{total_rain:.0f} mm")
col4.metric("💨 Avg Wind Speed", f"{avg_wind:.2f} kph")


# ---------------- CONVERT COUNTRY TO ISO ----------------
def get_iso3(country):
    try:
        return pycountry.countries.lookup(country).alpha_3
    except:
        return None

df["iso3"] = df["country"].apply(get_iso3)


# ---------------- CHOROPLETH MAP ----------------
st.subheader("🌍 Global Temperature Distribution")

fig = px.choropleth(
    df,
    locations="iso3",
    color="temperature_celsius",
    hover_name="country",
    animation_frame="year",
    color_continuous_scale="RdYlBu_r",
    title="Global Temperature Distribution Over Time"
)

fig.update_layout(
    title_font_size=24,
    coloraxis_colorbar=dict(title="Temp (°C)")
)

st.plotly_chart(fig, use_container_width=True)


# ---------------- TOP HOTTEST COUNTRIES ----------------
st.subheader("🔥 Top 10 Hottest Countries")

top_hot = df.groupby("country")["temperature_celsius"].mean().reset_index()

fig2 = px.bar(
    top_hot.sort_values("temperature_celsius", ascending=False).head(10),
    x="country",
    y="temperature_celsius",
    color="temperature_celsius",
    color_continuous_scale="Reds",
    title="Average Temperature by Country"
)

st.plotly_chart(fig2, use_container_width=True)


# ---------------- INSIGHT BOX ----------------
st.markdown(
"""
### 📊 Key Insights

• Global temperatures show strong seasonal variation across regions.  
• Some countries consistently experience higher average temperatures.  
• Climate patterns can be observed over time using the animated map.  
"""
)