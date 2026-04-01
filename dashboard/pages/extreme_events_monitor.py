import streamlit as st
import pandas as pd
import plotly.express as px


def show_page():

    st.header("🚨 Extreme Events Monitor")
    st.caption("Extreme events are defined as: Temperature > 40°C, Rainfall > 100 mm, Wind Speed > 60 kph")

    # -------------------------
    # LOAD DATA
    # -------------------------

    @st.cache_data
    def load_data():
        return pd.read_csv("data/processed/processed_weather_final.csv")

    df = load_data()

    # -------------------------
    # SIDEBAR FILTERS
    # -------------------------

    st.sidebar.header("Extreme Event Filters")

    all_countries = sorted(df["country"].unique())

    select_all = st.sidebar.checkbox("Select All Countries", value=True)

    countries = st.sidebar.multiselect(
        "Select Countries",
        all_countries,
        default=all_countries if select_all else []
    )

    if select_all or not countries:
        countries = all_countries

    year_range = st.sidebar.slider(
        "Year Range",
        int(df["year"].min()),
        int(df["year"].max()),
        (int(df["year"].min()), int(df["year"].max()))
    )

    filtered_df = df[
        (df["country"].isin(countries)) &
        (df["year"].between(year_range[0], year_range[1]))
    ]

    # -------------------------
    # DEFINE EXTREME EVENTS
    # -------------------------

    filtered_df["heatwave"] = filtered_df["temperature_celsius"] > 40
    filtered_df["heavy_rain"] = filtered_df["precip_mm"] > 100
    filtered_df["high_wind"] = filtered_df["wind_kph"] > 60

    # -------------------------
    # KPI CALCULATIONS
    # -------------------------

    heatwave_days = filtered_df["heatwave"].sum()
    heavy_rain_events = filtered_df["heavy_rain"].sum()
    high_wind_events = filtered_df["high_wind"].sum()

    total_events = heatwave_days + heavy_rain_events + high_wind_events

    risk_country = (
        filtered_df.groupby("country")[
            ["heatwave","heavy_rain","high_wind"]
        ].sum().sum(axis=1).idxmax()
    )

    # -------------------------
    # KPI CARDS
    # -------------------------

    st.subheader("Extreme Event Indicators")

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.metric("Total Extreme Events", total_events)

    with col2:
        st.metric("Heatwave Days", heatwave_days)

    with col3:
        st.metric("Heavy Rain Events", heavy_rain_events)

    with col4:
        st.metric("High Wind Events", high_wind_events)

    with col5:
        st.metric("Highest Risk Country", risk_country)

    st.divider()

    # -------------------------
    # EXTREME EVENTS TIMELINE
    # -------------------------

    timeline = (
        filtered_df.groupby("year")[
            ["heatwave","heavy_rain","high_wind"]
        ].sum().reset_index()
    )

    fig_timeline = px.line(
        timeline,
        x="year",
        y=["heatwave","heavy_rain","high_wind"],
        markers=True,
        title="Extreme Events Over Time"
    )

    st.plotly_chart(fig_timeline, use_container_width=True)

    # -------------------------
    # COUNTRY EVENT MAP
    # -------------------------

    map_data = (
        filtered_df.groupby("country")[
            ["heatwave","heavy_rain","high_wind"]
        ].sum().sum(axis=1).reset_index(name="events")
    )

    fig_map = px.choropleth(
        map_data,
        locations="country",
        locationmode="country names",
        color="events",
        color_continuous_scale="Reds",
        title="Extreme Events by Country"
    )

    st.plotly_chart(fig_map, use_container_width=True)

    # -------------------------
    # MONTHLY HEATMAP
    # -------------------------

    heatmap_data = (
        filtered_df.groupby(["year","month"])[
            ["heatwave","heavy_rain","high_wind"]
        ].sum().sum(axis=1).reset_index(name="events")
    )

    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x="month",
        y="year",
        z="events",
        color_continuous_scale="Reds",
        title="Monthly Extreme Events Heatmap"
    )

    # -------------------------
    # EVENT TYPE DISTRIBUTION
    # -------------------------

    event_counts = pd.DataFrame({
        "Event":["Heatwave","Heavy Rain","High Wind"],
        "Count":[heatwave_days,heavy_rain_events,high_wind_events]
    })

    colA,colB = st.columns(2)

    with colA:
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with colB:

        fig_pie = px.pie(
            event_counts,
            names="Event",
            values="Count",
            title="Extreme Event Distribution"
        )

        st.plotly_chart(fig_pie, use_container_width=True)