import streamlit as st
import plotly.express as px

from utils import CLIMATE_CONTINUOUS, CLIMATE_PALETTE


def render(df, selected_country="All", selected_year="All"):
    st.title("🌡 Temperature Intelligence")
    st.write("This section analyzes temperature patterns, seasonal trends and anomalies.")

    filtered = df.copy()
    if selected_country != "All":
        filtered = filtered[filtered["country"] == selected_country]
    if selected_year != "All":
        filtered = filtered[filtered["year"] == selected_year]

    # KPIs
    avg_temp = filtered["temperature_celsius"].mean()
    max_temp = filtered["temperature_celsius"].max()
    min_temp = filtered["temperature_celsius"].min()

    baseline = filtered["temperature_celsius"].mean()
    current = filtered[filtered["year"] == filtered["year"].max()]["temperature_celsius"].mean()

    anomaly = current - baseline

    trend = filtered.groupby("year")["temperature_celsius"].mean()

    if len(trend) >= 5:
        five_year = ((trend.iloc[-1] - trend.iloc[-5]) / trend.iloc[-5]) * 100
    else:
        five_year = 0

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Avg Temp", round(avg_temp, 2))
    c2.metric("Max Temp", round(max_temp, 2))
    c3.metric("Min Temp", round(min_temp, 2))
    c4.metric("Temperature Anomaly", round(anomaly, 2))
    c5.metric("5-Year Trend %", round(five_year, 2))

    # ---------------- TIME SERIES ----------------
    st.subheader("Temperature Trend")

    trend_df = filtered.groupby("year")["temperature_celsius"].mean().reset_index()

    fig = px.line(
        trend_df,
        x="year",
        y="temperature_celsius",
        color_discrete_sequence=CLIMATE_PALETTE,
    )
    st.plotly_chart(fig, width="stretch", key="temp_trend")

    st.info("Insight: This trend illustrates long-term temperature change patterns.")

    # ---------------- HEATMAP ----------------
    st.subheader("Seasonal Temperature Heatmap")

    heat = filtered.pivot_table(values="temperature_celsius", index="year", columns="month")

    fig2 = px.imshow(
        heat,
        aspect="auto",
        color_continuous_scale=CLIMATE_CONTINUOUS,
    )
    st.plotly_chart(fig2, width="stretch", key="temp_heatmap")

    st.info("Insight: Seasonal patterns become visible with hotter months showing stronger intensity.")

    # ---------------- HISTOGRAM ----------------
    st.subheader("Temperature Distribution")

    hist = px.histogram(
        filtered,
        x="temperature_celsius",
        nbins=40,
        color_discrete_sequence=CLIMATE_PALETTE,
    )
    st.plotly_chart(hist, width="stretch", key="temp_dist")

    st.info("Insight: This distribution shows how frequently temperature values occur globally.")

    # ---------------- MULTI COUNTRY COMPARISON ----------------
    st.subheader("Country Temperature Comparison")

    countries = st.multiselect("Select Countries", sorted(df["country"].unique()))

    if countries:
        comp = df[df["country"].isin(countries)]

        fig3 = px.line(
            comp,
            x="year",
            y="temperature_celsius",
            color="country",
            color_discrete_sequence=CLIMATE_PALETTE,
        )
        st.plotly_chart(fig3, width="stretch", key="temp_multi_comp")

        st.info("Insight: Comparing countries helps identify regional climate differences.")

    st.markdown(
        "<div style='text-align:center; margin-top:2rem; font-size:0.9rem; color:rgba(255,255,255,0.8);'>"
        "<a href='#top' style='color:#80d4ff; text-decoration:none;'>⬆ Back to top</a>"
        "</div>",
        unsafe_allow_html=True,
    )
