import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show_page():

    st.header("🌍 Regional Climate Comparison")

    # -------------------------
    # LOAD DATA
    # -------------------------

    @st.cache_data
    def load_data():
        return pd.read_csv("data/processed/processed_weather_final.csv")

    df = load_data()

    # -------------------------
    # COUNTRY SELECTION
    # -------------------------

    countries = sorted(df["country"].unique())

    st.sidebar.header("Regional Comparison")

    country_a = st.sidebar.selectbox(
        "Country A",
        countries
    )

    country_b = st.sidebar.selectbox(
        "Country B",
        countries,
        index=1 if len(countries) > 1 else 0
    )

    df_a = df[df["country"] == country_a]
    df_b = df[df["country"] == country_b]

    # -------------------------
    # KPI CALCULATIONS
    # -------------------------

    avg_temp_a = df_a["temperature_celsius"].mean()
    avg_temp_b = df_b["temperature_celsius"].mean()

    rain_a = df_a["precip_mm"].mean()
    rain_b = df_b["precip_mm"].mean()

    wind_a = df_a["wind_kph"].mean()
    wind_b = df_b["wind_kph"].mean()

    humidity_a = df_a["humidity"].mean()
    humidity_b = df_b["humidity"].mean()

    # -------------------------
    # KPI DISPLAY
    # -------------------------

    st.subheader("Country Climate Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Temperature Difference",
            f"{avg_temp_a - avg_temp_b:.2f} °C"
        )

    with col2:
        st.metric(
            "Rainfall Difference",
            f"{rain_a - rain_b:.2f} mm"
        )

    with col3:
        st.metric(
            "Wind Speed Difference",
            f"{wind_a - wind_b:.2f} kph"
        )

    with col4:
        st.metric(
            "Humidity Difference",
            f"{humidity_a - humidity_b:.2f} %"
        )

    st.divider()

    # -------------------------
    # TREND COMPARISON
    # -------------------------

    st.subheader("Climate Trend Comparison")

    metric = st.radio(
        "Select Climate Metric",
        ["Temperature", "Rainfall", "Wind Speed", "Humidity"],
        horizontal=True
    )

    # map metric to column
    if metric == "Temperature":
        value_column = "temperature_celsius"

    elif metric == "Rainfall":
        value_column = "precip_mm"

    elif metric == "Wind Speed":
        value_column = "wind_kph"

    else:
        value_column = "humidity"

    # prepare trend data
    trend_data = (
        df[df["country"].isin([country_a, country_b])]
        .groupby(["year", "country"])[value_column]
        .mean()
        .reset_index()
    )

    # create trend chart
    fig_trend = px.line(
        trend_data,
        x="year",
        y=value_column,
        color="country",
        markers=True,
        title=f"{metric} Trend Comparison"
    )

    st.plotly_chart(fig_trend, use_container_width=True)



    # -------------------------
    # METRIC BAR COMPARISON
    # -------------------------

    st.subheader("Climate Metric Comparison")

    metric_df = pd.DataFrame({
        "Metric": ["Temperature", "Rainfall", "Wind Speed", "Humidity"],
        country_a: [avg_temp_a, rain_a, wind_a, humidity_a],
        country_b: [avg_temp_b, rain_b, wind_b, humidity_b]
    })

    fig_bar = px.bar(
        metric_df,
        x="Metric",
        y=[country_a, country_b],
        barmode="group",
        title="Climate Metrics by Country"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # -------------------------
    # RADAR CHART
    # -------------------------

    st.subheader("Climate Profile Radar")

    categories = ["Temperature", "Rainfall", "Wind Speed", "Humidity"]

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=[avg_temp_a, rain_a, wind_a, humidity_a],
        theta=categories,
        fill='toself',
        name=country_a
    ))

    fig_radar.add_trace(go.Scatterpolar(
        r=[avg_temp_b, rain_b, wind_b, humidity_b],
        theta=categories,
        fill='toself',
        name=country_b
    ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title="Country Climate Radar Comparison"
    )

    st.plotly_chart(fig_radar, use_container_width=True)