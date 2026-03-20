# import streamlit as st
# import plotly.express as px
# import pycountry
# from utils.load_data import load_data
# import numpy as np

# st.title("🌍 Executive Climate Overview")

# df = load_data()

# # ---------------- SIDEBAR FILTERS ----------------
# st.sidebar.title("🔍 Filters")

# countries = st.sidebar.multiselect(
#     "Select Countries",
#     df["country"].unique(),
#     default=df["country"].unique()[:5]
# )

# year_range = st.sidebar.slider(
#     "Year Range",
#     int(df["year"].min()),
#     int(df["year"].max()),
#     (int(df["year"].min()), int(df["year"].max()))
# )

# df = df[(df["country"].isin(countries)) & (df["year"].between(*year_range))]

# # ---------------- KPI ----------------
# avg_temp = df["temperature_celsius"].mean()
# max_temp = df["temperature_celsius"].max()
# total_rain = df["precip_mm"].sum()
# avg_wind = df["wind_kph"].mean()

# col1, col2, col3, col4 = st.columns(4)

# col1.metric("🌡 Avg Temp", f"{avg_temp:.2f} °C")
# col2.metric("🔥 Max Temp", f"{max_temp:.2f} °C")
# col3.metric("🌧 Rainfall", f"{total_rain:.0f} mm")
# col4.metric("💨 Wind", f"{avg_wind:.2f} kph")

# # ---------------- ISO ----------------
# def get_iso3(country):
#     try:
#         return pycountry.countries.lookup(country).alpha_3
#     except:
#         return None

# df["iso3"] = df["country"].apply(get_iso3)

# # ---------------- MAP ----------------
# fig = px.scatter_geo(
#     df,
#     locations="iso3",
#     color="temperature_celsius",
#     size="precip_mm",
#     hover_name="country",
#     title="🌍 Climate Intensity Map"
# )

# st.plotly_chart(fig, use_container_width=True)

# # ---------------- AI INSIGHTS ----------------
# st.subheader("🧠 AI Insights")

# hottest = df.groupby("country")["temperature_celsius"].mean().idxmax()
# coldest = df.groupby("country")["temperature_celsius"].mean().idxmin()

# st.success(f"🔥 Hottest Country: {hottest}")
# st.success(f"❄️ Coldest Country: {coldest}")

# # ---------------- DOWNLOAD ----------------
# st.download_button("📥 Download Data", df.to_csv(index=False))


import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import pandas as pd
from utils.load_data import load_data

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Executive Climate Overview",
    page_icon="🌍",
    layout="wide"
)

px.defaults.template = "plotly_dark"

st.title("🌍 Executive Climate Overview")

st.markdown("""
High-level global climate insights with **key indicators, geospatial patterns,  
and comparative analysis across countries**.
""")

# ---------------- LOAD DATA ----------------
df = load_data()

# ---------------- FILTERS ----------------
st.sidebar.header("🌐 Global Filters")

all_countries = sorted(df["country"].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    ["All"] + all_countries,
    default=["All"]
)

# Fix conflict
if "All" in selected_countries and len(selected_countries) > 1:
    selected_countries = ["All"]

year_range = st.sidebar.slider(
    "Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

# Apply filters
if "All" in selected_countries:
    filtered_df = df.copy()
else:
    filtered_df = df[df["country"].isin(selected_countries)]

filtered_df = filtered_df[
    filtered_df["year"].between(year_range[0], year_range[1])
]

# ---------------- KPI SECTION ----------------
st.subheader("📊 Global Climate KPIs")

col1, col2, col3, col4 = st.columns(4)

avg_temp = filtered_df["temperature_celsius"].mean()

col1.metric("🌡 Avg Temperature", f"{avg_temp:.2f} °C")
col2.metric("🔥 Max Temperature", f"{filtered_df['temperature_celsius'].max():.2f} °C")
col3.metric("🌧 Total Rainfall", f"{filtered_df['precip_mm'].sum():.0f} mm")
col4.metric("💨 Avg Wind Speed", f"{filtered_df['wind_kph'].mean():.2f} kph")

# ---------------- GAUGE ----------------
st.subheader("🌡 Global Temperature Indicator")

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_temp,
    title={'text': "Avg Global Temperature"},
    gauge={
        'axis': {'range': [None, 50]},
        'bar': {'color': "red"},
        'steps': [
            {'range': [0, 20], 'color': "lightblue"},
            {'range': [20, 35], 'color': "orange"},
            {'range': [35, 50], 'color': "red"}
        ],
    }
))

st.plotly_chart(fig_gauge, use_container_width=True)

# ---------------- MAP ----------------
st.subheader("🌍 Global Climate Map")

def get_iso3(country):
    try:
        return pycountry.countries.lookup(country).alpha_3
    except:
        return None

filtered_df["iso3"] = filtered_df["country"].apply(get_iso3)

fig_map = px.scatter_geo(
    filtered_df,
    locations="iso3",
    color="temperature_celsius",
    size="precip_mm",
    hover_name="country",
    title="Climate Intensity Map"
)

st.plotly_chart(fig_map, use_container_width=True)

# ---------------- TOP VS BOTTOM ----------------
st.subheader("⚖️ Temperature Extremes Comparison")

temp_avg = filtered_df.groupby("country")["temperature_celsius"].mean()

top = temp_avg.nlargest(5)
bottom = temp_avg.nsmallest(5)

compare_df = pd.concat([top, bottom]).reset_index()

fig_bar = px.bar(
    compare_df,
    x="country",
    y="temperature_celsius",
    color="temperature_celsius",
    title="Top & Bottom Temperature Countries"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ---------------- DISTRIBUTION ----------------
st.subheader("📊 Temperature Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="temperature_celsius",
    nbins=30,
    color="country",
    title="Temperature Distribution"
)

st.plotly_chart(fig_hist, use_container_width=True)

# ---------------- GLOBAL TREND ----------------
st.subheader("📈 Global Temperature Trend")

trend_df = filtered_df.groupby("year")["temperature_celsius"].mean().reset_index()

fig_trend = px.line(
    trend_df,
    x="year",
    y="temperature_celsius",
    markers=True,
    title="Average Temperature Over Time"
)

st.plotly_chart(fig_trend, use_container_width=True)

# ---------------- AI INSIGHTS ----------------
st.subheader("🧠 Key Insights")

if len(filtered_df) > 0:
    hottest = temp_avg.idxmax()
    coldest = temp_avg.idxmin()
    rainy = filtered_df.groupby("country")["precip_mm"].sum().idxmax()

    st.success(f"🔥 Hottest Country: {hottest}")
    st.success(f"❄️ Coldest Country: {coldest}")
    st.success(f"🌧 Highest Rainfall: {rainy}")
else:
    st.warning("No data available for selected filters")