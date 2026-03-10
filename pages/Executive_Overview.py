import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(page_title="ClimateScope Dashboard", layout="wide")

st.title("🌍 ClimateScope – Executive Overview")

# ------------------------------------------------
# Load Dataset
# ------------------------------------------------
df = pd.read_csv("D:/climateScope/data/processed/cleaned_global__weather.csv")

df["last_updated"] = pd.to_datetime(df["last_updated"])
df["year"] = df["last_updated"].dt.year
df["date"] = df["last_updated"].dt.date

# ------------------------------------------------
# Sidebar Filters
# ------------------------------------------------
st.sidebar.header("🔎 Global Filters")

country = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(df["country"].unique())
)

year_range = st.sidebar.slider(
    "Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df["date"].min(), df["date"].max()]
)

# ------------------------------------------------
# Apply Filters
# ------------------------------------------------
filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["date"] >= date_range[0]) &
    (df["date"] <= date_range[1])
]

if country != "All":
    filtered_df = filtered_df[filtered_df["country"] == country]

# ------------------------------------------------
# KPI Calculations
# ------------------------------------------------
avg_temp = filtered_df["temperature_celsius"].mean()

total_rain = filtered_df["precip_mm"].sum()

avg_wind = filtered_df["wind_kph"].mean()

extreme_events = filtered_df[
    (filtered_df["temperature_celsius"] > 40) |
    (filtered_df["precip_mm"] > 100) |
    (filtered_df["wind_kph"] > 60)
].shape[0]

# Hottest Country
hottest_country = (
    filtered_df.groupby("country")["temperature_celsius"]
    .mean()
    .idxmax()
)

# ------------------------------------------------
# Temperature YoY Change
# ------------------------------------------------
yearly_temp = (
    filtered_df.groupby("year")["temperature_celsius"]
    .mean()
    .reset_index()
)

if len(yearly_temp) > 1:
    yoy_change = (
        (yearly_temp.iloc[-1]["temperature_celsius"] -
         yearly_temp.iloc[-2]["temperature_celsius"]) /
         yearly_temp.iloc[-2]["temperature_celsius"]
    ) * 100
else:
    yoy_change = 0

# ------------------------------------------------
# KPI Layout
# ------------------------------------------------
st.subheader("📊 Global Climate KPIs")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("🌡 Global Avg Temp", f"{avg_temp:.2f} °C")
col2.metric("📈 Temp Change (YoY)", f"{yoy_change:.2f} %")
col3.metric("🌧 Total Precipitation", f"{total_rain:.0f} mm")
col4.metric("💨 Avg Wind Speed", f"{avg_wind:.2f} kph")
col5.metric("🚨 Extreme Events", extreme_events)
col6.metric("🔥 Hottest Country", hottest_country)

st.divider()

# ------------------------------------------------
# Insight Summary Box
# ------------------------------------------------
st.info(
"""
📌 **Key Insights**

• Global temperature shows steady variation across years.  
• Extreme events are strongly associated with high rainfall and wind spikes.  
• Certain regions consistently record higher average temperatures.  
• Climate patterns show seasonal and regional variability.
"""
)

# ------------------------------------------------
# Charts Layout
# ------------------------------------------------
colA, colB = st.columns(2)

# ---------------- Map ----------------
with colA:

    st.subheader("🌍 Global Temperature Map")

    map_data = (
        filtered_df.groupby("country")["temperature_celsius"]
        .mean()
        .reset_index()
    )

    fig_map = px.choropleth(
        map_data,
        locations="country",
        locationmode="country names",
        color="temperature_celsius",
        color_continuous_scale="RdYlBu_r"
    )

    st.plotly_chart(fig_map, use_container_width=True)

# ---------------- Trend ----------------
with colB:

    st.subheader("📈 Global Temperature Trend")

    fig_trend = px.line(
        yearly_temp,
        x="year",
        y="temperature_celsius",
        markers=True
    )

    st.plotly_chart(fig_trend, use_container_width=True)

# ------------------------------------------------
# Top 5 High Temperature Countries
# ------------------------------------------------
st.subheader("🔥 Top 5 High Temperature Countries")

top5 = (
    filtered_df.groupby("country")["temperature_celsius"]
    .mean()
    .nlargest(5)
    .reset_index()
)

fig_bar = px.bar(
    top5,
    x="country",
    y="temperature_celsius",
    color="temperature_celsius",
    color_continuous_scale="OrRd"
)

st.plotly_chart(fig_bar, use_container_width=True)