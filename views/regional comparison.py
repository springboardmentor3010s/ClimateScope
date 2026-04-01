import streamlit as st
import plotly.express as px

from utils import CLIMATE_PALETTE


def render(df, selected_country="All", selected_year="All"):
    st.title("🌍 Regional Climate Comparison")
    st.write("Compare climate indicators across countries to understand regional differences.")

    filtered = df.copy()
    if selected_country != "All":
        filtered = filtered[filtered["country"] == selected_country]
    if selected_year != "All":
        filtered = filtered[filtered["year"] == selected_year]

    countries = sorted(filtered["country"].unique())

    if len(countries) < 2:
        st.warning("Select a country and/or year that contains at least two countries of data.")
        return

    col1, col2 = st.columns(2)

    countryA = col1.selectbox("Country A", countries, index=0)
    countryB = col2.selectbox("Country B", countries, index=min(1, len(countries) - 1))

    dataA = filtered[filtered["country"] == countryA]
    dataB = filtered[filtered["country"] == countryB]

    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Country A Avg Temp", round(dataA["temperature_celsius"].mean(), 2))
    c2.metric("Country B Avg Temp", round(dataB["temperature_celsius"].mean(), 2))

    temp_diff = dataA["temperature_celsius"].mean() - dataB["temperature_celsius"].mean()
    c3.metric("Temp Difference", round(temp_diff, 2))

    rain_diff = dataA["precip_mm"].mean() - dataB["precip_mm"].mean()
    wind_diff = dataA["wind_kph"].mean() - dataB["wind_kph"].mean()

    st.write("Rainfall Difference:", round(rain_diff, 2))
    st.write("Wind Difference:", round(wind_diff, 2))

    # Dual Line Comparison
    st.subheader("Temperature Trend Comparison")
    comp = filtered[filtered["country"].isin([countryA, countryB])]

    fig = px.line(
        comp,
        x="year",
        y="temperature_celsius",
        color="country",
        color_discrete_sequence=CLIMATE_PALETTE,
    )
    st.plotly_chart(fig, width="stretch", key="reg_temp_comp")

    st.info("Insight: This chart shows how temperature trends differ between two regions.")

    # Bar Comparison
    st.subheader("Rainfall Comparison")
    bar_data = {
        "Country": [countryA, countryB],
        "Rainfall": [dataA["precip_mm"].mean(), dataB["precip_mm"].mean()],
    }

    fig2 = px.bar(
        bar_data,
        x="Country",
        y="Rainfall",
        color_discrete_sequence=CLIMATE_PALETTE,
    )
    st.plotly_chart(fig2, width="stretch", key="reg_rain_comp")

    st.info("Insight: Rainfall differences can influence agriculture and ecosystem stability.")

    # Radar Chart
    st.subheader("Climate Indicator Radar")
    radar_data = {
        "Metric": ["Temperature", "Rainfall", "Wind"],
        countryA: [
            dataA["temperature_celsius"].mean(),
            dataA["precip_mm"].mean(),
            dataA["wind_kph"].mean(),
        ],
        countryB: [
            dataB["temperature_celsius"].mean(),
            dataB["precip_mm"].mean(),
            dataB["wind_kph"].mean(),
        ],
    }

    fig3 = px.line_polar(
        radar_data,
        r=countryA,
        theta="Metric",
        line_close=True,
        color_discrete_sequence=CLIMATE_PALETTE,
    )
    st.plotly_chart(fig3, width="stretch", key="reg_radar")

    st.info("Insight: Radar visualization highlights overall climate profile differences.")

    st.markdown(
        "<div style='text-align:center; margin-top:2rem; font-size:0.9rem; color:rgba(255,255,255,0.8);'>"
        "<a href='#top' style='color:#80d4ff; text-decoration:none;'>⬆ Back to top</a>"
        "</div>",
        unsafe_allow_html=True,
    )
