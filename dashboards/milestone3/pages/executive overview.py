import streamlit as st
import plotly.express as px

from utils import CLIMATE_CONTINUOUS, CLIMATE_PALETTE


def render(df, selected_country="All", selected_year="All"):
    st.title("🌍 Executive Climate Overview")
    st.write("This page summarizes global climate conditions using key indicators and high-level visual insights.")

    filtered = df.copy()
    if selected_country != "All":
        filtered = filtered[filtered["country"] == selected_country]
    if selected_year != "All":
        filtered = filtered[filtered["year"] == selected_year]

    # ---------------- KPIs ----------------
    avg_temp = filtered["temperature_celsius"].mean()
    total_rain = filtered["precip_mm"].sum()
    avg_wind = filtered["wind_kph"].mean()

    extreme = filtered[
        (filtered["temperature_celsius"] > 40)
        | (filtered["precip_mm"] > 100)
        | (filtered["wind_kph"] > 60)
    ]

    yearly = filtered.groupby("year")["temperature_celsius"].mean()
    if len(yearly) > 1:
        yoy = ((yearly.iloc[-1] - yearly.iloc[-2]) / yearly.iloc[-2]) * 100
    else:
        yoy = 0

    hottest_country = "—"
    if not filtered.empty:
        hottest_country = (
            filtered.groupby("country")["temperature_celsius"].mean().idxmax()
        )

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric("🌡 Global Avg Temp", round(avg_temp, 2))
    c2.metric("📈 Temp Change YoY %", round(yoy, 2))
    c3.metric("🌧 Total Precipitation", round(total_rain, 2))
    c4.metric("💨 Avg Wind Speed", round(avg_wind, 2))
    c5.metric("🚨 Extreme Events", len(extreme))
    c6.metric("🔥 Hottest Country", hottest_country)

    # ---------------- CHOROPLETH MAP ----------------
    st.subheader("Global Temperature Map")

    country_avg = filtered.groupby("country")["temperature_celsius"].mean().reset_index()

    fig = px.choropleth(
        country_avg,
        locations="country",
        locationmode="country names",
        color="temperature_celsius",
        title="Average Temperature by Country",
        color_continuous_scale=CLIMATE_CONTINUOUS,
    )

    st.plotly_chart(fig, width="stretch", key="exec_temp_map")
    st.info("Insight: Countries closer to the equator generally show higher average temperatures.")

    # ---------------- TEMPERATURE TREND ----------------
    st.subheader("Global Temperature Trend")

    trend = filtered.groupby("year")["temperature_celsius"].mean().reset_index()

    fig2 = px.line(
        trend,
        x="year",
        y="temperature_celsius",
        markers=True,
        color_discrete_sequence=CLIMATE_PALETTE,
    )
    st.plotly_chart(fig2, width="stretch", key="exec_temp_trend")

    st.info("Insight: The long-term trend highlights how global temperatures change across years.")

    # ---------------- TOP COUNTRIES ----------------
    st.subheader("Top 5 Hottest Countries")

    top5 = filtered.groupby("country")["temperature_celsius"].mean().nlargest(5).reset_index()

    fig3 = px.bar(
        top5,
        x="country",
        y="temperature_celsius",
        color="temperature_celsius",
        color_discrete_sequence=CLIMATE_PALETTE,
    )
    st.plotly_chart(fig3, width="stretch", key="exec_top5")

    st.info("Insight: These countries experience the highest average temperatures in the selected period.")

    st.markdown(
        "<div style='text-align:center; margin-top:2rem; font-size:0.9rem; color:rgba(255,255,255,0.8);'>"
        "<a href='#top' style='color:#80d4ff; text-decoration:none;'>⬆ Back to top</a>"
        "</div>",
        unsafe_allow_html=True,
    )
