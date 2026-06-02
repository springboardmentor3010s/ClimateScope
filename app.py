import streamlit as st
from data_loader import load_data
from filters import apply_filters
from visualizations import show_charts

st.set_page_config(
    page_title="🌍 Climate Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# HEADER
st.title("🌍 Climate Intelligence Dashboard")
st.markdown("### 📊 Advanced Weather Analytics & Insights")

# LOAD DATA
df = load_data()

# FILTERS
filtered_df = apply_filters(df)

# DASHBOARD
show_charts(filtered_df)

# FOOTER SECTION
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Data Preview")
    st.dataframe(filtered_df)

with col2:
    st.subheader("⬇ Export Data")
    st.download_button(
        "Download CSV",
        filtered_df.to_csv(index=False),
        file_name="weather_data.csv"
    )

# AUTO INSIGHTS
st.subheader("🧠 AI Insights")

hottest = filtered_df.loc[filtered_df["temperature_celsius"].idxmax()]
coldest = filtered_df.loc[filtered_df["temperature_celsius"].idxmin()]

st.write(f"🔥 Hottest Location: **{hottest['location_name']} ({hottest['temperature_celsius']}°C)**")
st.write(f"❄ Coldest Location: **{coldest['location_name']} ({coldest['temperature_celsius']}°C)**")