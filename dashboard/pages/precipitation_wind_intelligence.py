import streamlit as st
import pandas as pd
import plotly.express as px


def show_page():

    st.header("🌧 Precipitation & Wind Intelligence")

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

    st.sidebar.header("Rain & Wind Filters")

    # -------------------------
    # COUNTRY FILTER
    # -------------------------

    all_countries = sorted(df["country"].unique())

    select_all = st.sidebar.checkbox("Select All Countries", value=True)

    countries = st.sidebar.multiselect(
        "Select Countries",
        all_countries,
        default=all_countries if select_all else []
    )

    # if nothing selected OR checkbox active → use all countries
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
    # KPI CALCULATIONS
    # -------------------------

    total_rain = filtered_df["precip_mm"].sum()
    avg_rain = filtered_df["precip_mm"].mean()
    avg_wind = filtered_df["wind_kph"].mean()
    rain_variability = filtered_df["precip_mm"].std()

    heavy_rain_days = filtered_df[filtered_df["precip_mm"] > 50].shape[0]
    high_wind_events = filtered_df[filtered_df["wind_kph"] > 40].shape[0]

    # -------------------------
    # KPI CARDS
    # -------------------------

    st.subheader("Rain & Wind Indicators")

    col1,col2,col3,col4,col5,col6 = st.columns(6)

    with col1:
        st.metric("Total Rainfall", f"{total_rain:.0f} mm")

    with col2:
        st.metric("Average Rainfall", f"{avg_rain:.2f} mm")

    with col3:
        st.metric("Average Wind Speed", f"{avg_wind:.2f} kph")

    with col4:
        st.metric("Heavy Rain Days", heavy_rain_days)

    with col5:
        st.metric("High Wind Events", high_wind_events)
    
    with col6:
        st.metric("Rainfall Variability", f"{rain_variability:.2f}")

    st.divider()

    # -------------------------
    # RAIN & WIND TRENDS
    # -------------------------

    trend_data = (
        filtered_df.groupby("year")
        .agg({
            "precip_mm":"mean",
            "wind_kph":"mean"
        })
        .reset_index()
    )

    colA,colB = st.columns(2)

    with colA:

        fig_rain = px.line(
            trend_data,
            x="year",
            y="precip_mm",
            markers=True,
            title="Rainfall Trend"
        )

        st.plotly_chart(fig_rain, use_container_width=True)

    with colB:

        fig_wind = px.line(
            trend_data,
            x="year",
            y="wind_kph",
            markers=True,
            title="Wind Speed Trend"
        )

        st.plotly_chart(fig_wind, use_container_width=True)

    # -------------------------
    # RAIN VS WIND SCATTER
    # -------------------------

    st.subheader("Rainfall vs Wind Relationship")
    st.divider()

    fig_scatter = px.scatter(
        filtered_df,
        x="precip_mm",
        y="wind_kph",
        color="temperature_celsius",
        size="wind_kph",
        title="Rainfall vs Wind Speed Relationship",
        color_continuous_scale="thermal"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)


    st.subheader("Wind Direction Distribution")
    st.divider()

    fig_wind_dir = px.histogram(
        filtered_df,
        x="wind_direction",
        title="Wind Direction Frequency"
    )

    st.plotly_chart(fig_wind_dir, use_container_width=True)


    # -------------------------
    # HEAVY RAINFALL EVENTS
    # -------------------------

    st.subheader("Heavy Rainfall Events Timeline")
    st.divider()

    heavy_rain = filtered_df[filtered_df["precip_mm"] > 50]

    fig_heavy = px.scatter(
        heavy_rain,
        x="year",
        y="precip_mm",
        color="country",
        title="Heavy Rainfall Events Over Time"
    )

    st.plotly_chart(fig_heavy, use_container_width=True)

    # -------------------------
    # COUNTRY ANALYSIS
    # -------------------------

    colC,colD = st.columns(2)

    with colC:

        rainfall_country = (
            filtered_df.groupby("country")["precip_mm"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig_rain_country = px.bar(
            rainfall_country,
            x="country",
            y="precip_mm",
            title="Average Rainfall by Country"
        )

        st.plotly_chart(fig_rain_country, use_container_width=True)

    with colD:

        fig_wind_box = px.box(
            filtered_df,
            x="country",
            y="wind_kph",
            color="country",
            title="Wind Speed Distribution by Country"
        )

        st.plotly_chart(fig_wind_box, use_container_width=True)