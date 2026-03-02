import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="ClimateScope Dashboard",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
.main {
    background-color: #f4f6f9;
}
h1 {
    color: #1f4e79;
}
.section-header {
    font-size:22px;
    font-weight:600;
    color:#0e2a47;
    margin-top:30px;
}
.metric-box {
    background-color:#ffffff;
    padding:15px;
    border-radius:10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 ClimateScope – Global Climate Intelligence")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/processed_weather_final.csv")

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🔎 Global Filters")

all_countries = sorted(df['country'].unique())

select_all = st.sidebar.checkbox("Select All Countries")

if select_all:
    selected_countries = all_countries
else:
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        options=all_countries,
        default=all_countries[:5]
    )

selected_metric = st.sidebar.selectbox(
    "Select Climate Metric",
    [
        "temperature_celsius",
        "precip_mm",
        "wind_kph",
        "humidity"
    ]
)

filtered_df = df[df['country'].isin(selected_countries)]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------
st.markdown('<div class="section-header">📊 Key Climate Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Temp (°C)", round(filtered_df['temperature_celsius'].mean(), 2))
col2.metric("Avg Rain (mm)", round(filtered_df['precip_mm'].mean(), 2))
col3.metric("Avg Wind (km/h)", round(filtered_df['wind_kph'].mean(), 2))
col4.metric("Avg Humidity (%)", round(filtered_df['humidity'].mean(), 2))

st.divider()

# --------------------------------------------------
# Geographic View
# --------------------------------------------------
st.markdown('<div class="section-header">🗺 Geographic Distribution</div>', unsafe_allow_html=True)

country_avg = (
    filtered_df
    .groupby('country')[selected_metric]
    .mean()
    .reset_index()
)

fig_map = px.choropleth(
    country_avg,
    locations='country',
    locationmode='country names',
    color=selected_metric,
    color_continuous_scale='Turbo',
    title=f"{selected_metric} by Country"
)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# --------------------------------------------------
# Time Trend
# --------------------------------------------------
st.markdown('<div class="section-header">📈 Time Trend Analysis</div>', unsafe_allow_html=True)

monthly = (
    filtered_df
    .groupby(['year', 'month'])[selected_metric]
    .mean()
    .reset_index()
)

monthly['date'] = pd.to_datetime(
    monthly[['year', 'month']].assign(day=1)
)

fig_line = px.line(
    monthly,
    x='date',
    y=selected_metric,
    color_discrete_sequence=['#1f77b4']
)

st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# --------------------------------------------------
# Seasonal Comparison
# --------------------------------------------------
st.markdown('<div class="section-header">🌦 Seasonal Comparison</div>', unsafe_allow_html=True)

season_data = (
    filtered_df
    .groupby(['season', 'country'])[selected_metric]
    .mean()
    .reset_index()
)

season_pivot = season_data.pivot(
    index='country',
    columns='season',
    values=selected_metric
)

fig_heatmap = px.imshow(
    season_pivot,
    aspect="auto",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.divider()
