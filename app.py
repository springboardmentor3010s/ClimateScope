import streamlit as st
import pandas as pd

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="ClimateScope Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------------------------------
# Custom CSS (Professional SaaS Style)
# -----------------------------------------------------

st.markdown("""
<style>

.main-title{
    font-size:40px;
    font-weight:700;
}

.subtitle{
    font-size:18px;
    color:#BBBBBB;
}

.kpi-card{
    background-color:#161B22;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow:0px 0px 8px rgba(0,0,0,0.4);
}

.kpi-value{
    font-size:28px;
    font-weight:bold;
    color:#FF4B4B;
}

.kpi-label{
    font-size:14px;
    color:#CCCCCC;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("D:/climateScope/data/processed/cleaned_global__weather.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df["year"] = df["last_updated"].dt.year
    df["month"] = df["last_updated"].dt.month
    return df

df = load_data()

# -----------------------------------------------------
# Title Section
# -----------------------------------------------------

st.markdown('<div class="main-title">🌍 ClimateScope Dashboard</div>', unsafe_allow_html=True)

st.markdown(
"""
<div class="subtitle">
A global climate intelligence platform for analyzing temperature trends,
precipitation patterns, wind behavior, and climate risk indicators.
</div>
""",
unsafe_allow_html=True
)

st.divider()

# -----------------------------------------------------
# High Level KPIs
# -----------------------------------------------------

avg_temp = df["temperature_celsius"].mean()
avg_rain = df["precip_mm"].mean()
avg_wind = df["wind_kph"].mean()

extreme_events = df[
    (df["temperature_celsius"] > 40) |
    (df["precip_mm"] > 100) |
    (df["wind_kph"] > 60)
].shape[0]

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="kpi-card">
<div class="kpi-label">Global Avg Temperature</div>
<div class="kpi-value">{avg_temp:.2f} °C</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="kpi-card">
<div class="kpi-label">Avg Rainfall</div>
<div class="kpi-value">{avg_rain:.2f} mm</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="kpi-card">
<div class="kpi-label">Avg Wind Speed</div>
<div class="kpi-value">{avg_wind:.2f} kph</div>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="kpi-card">
<div class="kpi-label">Extreme Events</div>
<div class="kpi-value">{extreme_events}</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------
# Dashboard Navigation Section
# -----------------------------------------------------

st.markdown("## 📊 Dashboard Modules")

colA, colB, colC = st.columns(3)

with colA:
    st.info(
        """
        🌍 **Executive Overview**

        Global climate summary including:
        - Temperature trends
        - Global weather distribution
        - Extreme event indicators
        """
    )

    st.info(
        """
        🌡 **Temperature Intelligence**

        Deep analysis of temperature patterns:
        - Seasonal heatmaps
        - Temperature anomalies
        - Multi-country comparison
        """
    )

with colB:
    st.info(
        """
        🌧 **Precipitation & Wind**

        Rainfall and wind analysis:
        - Rainfall variability
        - Storm detection
        - Wind intensity trends
        """
    )

    st.info(
        """
        🚨 **Extreme Events Monitor**

        Climate alert monitoring:
        - Heatwaves
        - Heavy rainfall
        - Storm events
        """
    )

with colC:
    st.info(
        """
        🌍 **Regional Comparison**

        Side-by-side comparison of countries:
        - Temperature
        - Rainfall
        - Wind patterns
        """
    )

    st.info(
        """
        ⚠ **Climate Risk Intelligence**

        Decision support analytics:
        - Climate risk score
        - Risk heatmaps
        - High-risk regions
        """
    )

st.divider()

# -----------------------------------------------------
# Insight Section
# -----------------------------------------------------

st.markdown("## 📌 Key Insights")

st.success(
"""
• Global temperatures show increasing variability across regions.  
• Rainfall extremes are becoming more frequent in coastal zones.  
• Wind intensity spikes align with major storm events.  
• Climate risk scores highlight emerging high-risk regions.
"""
)

# -----------------------------------------------------
# Footer
# -----------------------------------------------------

st.markdown("---")
st.caption("ClimateScope | Global Climate Intelligence Dashboard")