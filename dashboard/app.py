import streamlit as st
from styles import load_css
import pages.executive_overview as executive
import pages.temperature_intelligence as temperature
import pages.precipitation_wind_intelligence as rain_wind
import pages.extreme_events_monitor as extreme_events
import pages.regional_comparison as regional
import pages.climate_risk_intelligence as risk


st.set_page_config(
    page_title="ClimateScope Dashboard",
    layout="wide"
)

load_css()

st.markdown("""
<h1 style='text-align:center;
background: linear-gradient(90deg,#6366f1,#06b6d4);
color:white;
padding:14px;
border-radius:10px;
font-weight:700'>
ClimateScope Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown(
"<p style='text-align:center; font-size:16px; color:#555;'>Executive Climate Intelligence Overview</p>",
unsafe_allow_html=True
)

# Top navigation
page = st.radio(
    "",
    ["Executive Overview","Temperature Intelligence",
     "Precipitation & Wind Intelligence",
     "Extreme Events Monitor",
     "Regional Comparison",
     "Climate Risk Intelligence"],
    horizontal=True
)

# Page routing
if page == "Executive Overview":
    executive.show_page()

elif page == "Temperature Intelligence":
    temperature.show_page()


elif page == "Precipitation & Wind Intelligence":
    rain_wind.show_page()

elif page == "Extreme Events Monitor":
    extreme_events.show_page()

elif page == "Regional Comparison":
    regional.show_page()

elif page == "Climate Risk Intelligence":
    risk.show_page()