import streamlit as st
import plotly.express as px

from utils import PW_PALETTE


def render(df, selected_country="All", selected_year="All"):
    st.title("🌧 Precipitation & Wind Intelligence")

    filtered = df.copy()
    if selected_country != "All":
        filtered = filtered[filtered["country"] == selected_country]
    if selected_year != "All":
        filtered = filtered[filtered["year"] == selected_year]

    total_rain = filtered["precip_mm"].sum()
    heavy_rain = filtered[filtered["precip_mm"] > 50].shape[0]
    avg_wind = filtered["wind_kph"].mean()
    high_wind = filtered[filtered["wind_kph"] > 60].shape[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Rainfall", round(total_rain, 2))
    c2.metric("Heavy Rain Days", heavy_rain)
    c3.metric("Avg Wind Speed", round(avg_wind, 2))
    c4.metric("High Wind Events", high_wind)

    # Rainfall Trend
    rain = filtered.groupby("year")["precip_mm"].mean().reset_index()

    fig = px.line(
        rain,
        x="year",
        y="precip_mm",
        color_discrete_sequence=PW_PALETTE,
    )
    st.plotly_chart(fig, width="stretch", key="pw_rain_trend")

    st.info("Insight: Rainfall trends highlight how precipitation changes across years.")

    # Wind Trend
    wind = filtered.groupby("year")["wind_kph"].mean().reset_index()

    fig2 = px.line(
        wind,
        x="year",
        y="wind_kph",
        color_discrete_sequence=PW_PALETTE,
    )
    st.plotly_chart(fig2, width="stretch", key="pw_wind_trend")

    st.info("Insight: Increasing wind trends may indicate stronger atmospheric disturbances.")

    # Scatter
    scatter = px.scatter(
        filtered,
        x="precip_mm",
        y="wind_kph",
        color_discrete_sequence=PW_PALETTE,
    )
    st.plotly_chart(scatter, width="stretch", key="pw_scatter")

    st.info("Insight: This chart reveals the relationship between rainfall intensity and wind speed.")

    # Ranking
    rank = filtered.groupby("country")["precip_mm"].mean().nlargest(10).reset_index()

    fig3 = px.bar(
        rank,
        x="country",
        y="precip_mm",
        color_discrete_sequence=PW_PALETTE,
    )
    st.plotly_chart(fig3, width="stretch", key="pw_rain_rank")

    st.info("Insight: Some countries consistently receive significantly higher rainfall.")

    st.markdown(
        "<div style='text-align:center; margin-top:2rem; font-size:0.9rem; color:rgba(255,255,255,0.8);'>"
        "<a href='#top' style='color:#80d4ff; text-decoration:none;'>⬆ Back to top</a>"
        "</div>",
        unsafe_allow_html=True,
    )
