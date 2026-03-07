import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Climate Scope Dashboard", layout="wide")

# ================= LOAD DATA =================
df = pd.read_csv("cleaned_weather.csv")
df['last_updated'] = pd.to_datetime(df['last_updated'])
df['month'] = df['last_updated'].dt.month

# ================= SIDEBAR =================
st.sidebar.title("🌍 Dashboard Controls")

countries = ["All"] + sorted(df['country'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", countries)

filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df['country'] == selected_country]

locations = ["All"] + sorted(filtered_df['location_name'].dropna().unique().tolist())
selected_location = st.sidebar.selectbox("Select Location", locations)

if selected_location != "All":
    filtered_df = filtered_df[filtered_df['location_name'] == selected_location]

section = st.sidebar.radio(
    "Navigate Dashboard",
    (
        "Geographical Analysis",
        "Climate Relationships",
        "Air Quality",
        "Trends"
    )
)

# ================= TITLE =================
st.title("🌦 Climate Scope")
st.caption("Global Weather & Air Quality Analytics Dashboard")

# ================= KPI CARDS (ALWAYS VISIBLE) =================
k1, k2, k3, k4 = st.columns(4)

k1.metric("Avg Temperature (°C)", round(filtered_df['temperature_celsius'].mean(), 2))
k2.metric("Avg Humidity (%)", round(filtered_df['humidity'].mean(), 2))
k3.metric("Avg Wind Speed (kph)", round(filtered_df['wind_kph'].mean(), 2))
k4.metric("Avg Pressure (mb)", round(filtered_df['pressure_mb'].mean(), 2))

st.markdown("---")

# ================= CHART AREA (CHANGES ONLY) =================

# -------- MAP --------
if section == "Geographical Analysis":

    st.subheader("🌍 Country-wise Temperature Distribution")

    map_fig = px.scatter_geo(
        filtered_df,
        lat="latitude",
        lon="longitude",
        color="temperature_celsius",
        hover_name="location_name",
        projection="natural earth"
    )
    st.plotly_chart(map_fig, use_container_width=True)

# -------- RELATIONSHIP --------
elif section == "Climate Relationships":

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🌡 Temperature vs Humidity")
        st.plotly_chart(
            px.scatter(
                filtered_df,
                x="temperature_celsius",
                y="humidity",
                color="humidity"
            ),
            use_container_width=True
        )

    with c2:
        st.subheader("📅 Monthly Temperature Pattern")
        monthly_avg = (
            filtered_df.groupby("month")["temperature_celsius"]
            .mean()
            .reset_index()
        )
        st.plotly_chart(
            px.bar(monthly_avg, x="month", y="temperature_celsius"),
            use_container_width=True
        )

# -------- AIR QUALITY --------
elif section == "Air Quality":

    st.subheader("🫁 Air Quality (PM2.5)")

    st.plotly_chart(
        px.bar(
            filtered_df,
            x="location_name",
            y="air_quality_pm2.5",
            color="air_quality_pm2.5"
        ),
        use_container_width=True
    )

# -------- TRENDS --------
elif section == "Trends":

    st.subheader("📈 Temperature Trend Over Time")

    st.plotly_chart(
        px.line(
            filtered_df,
            x="last_updated",
            y="temperature_celsius"
        ),
        use_container_width=True
    )