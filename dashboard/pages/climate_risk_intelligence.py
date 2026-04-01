import streamlit as st
import pandas as pd
import plotly.express as px


def show_page():

    st.header("⚠ Climate Risk Intelligence")

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

    st.sidebar.header("Risk Filters")

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
    # CALCULATE RISK SCORE
    # -------------------------

    risk_data = (
        filtered_df.groupby("country")[
            ["heatwave", "heavy_rain", "high_wind"]
        ]
        .sum()
        .reset_index()
    )

    risk_data["risk_score"] = (
        risk_data["heatwave"] +
        risk_data["heavy_rain"] +
        risk_data["high_wind"]
    )

    # -------------------------
    # KPI CALCULATIONS
    # -------------------------

    avg_risk = risk_data["risk_score"].mean()

    max_risk_country = risk_data.loc[
        risk_data["risk_score"].idxmax(), "country"
    ]

    total_events = risk_data["risk_score"].sum()

    high_risk_count = (risk_data["risk_score"] > avg_risk).sum()

    # -------------------------
    # KPI CARDS
    # -------------------------

    st.subheader("Climate Risk Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Average Risk Score", f"{avg_risk:.2f}")

    with col2:
        st.metric("Highest Risk Country", max_risk_country)

    with col3:
        st.metric("Total Extreme Events", total_events)

    with col4:
        st.metric("High Risk Countries", high_risk_count)

    st.divider()

    # -------------------------
    # RISK MAP
    # -------------------------

    st.subheader("Global Climate Risk Map")

    fig_map = px.choropleth(
        risk_data,
        locations="country",
        locationmode="country names",
        color="risk_score",
        color_continuous_scale="Reds",
        title="Climate Risk Score by Country"
    )

    st.plotly_chart(fig_map, use_container_width=True)

    # -------------------------
    # RISK TREND
    # -------------------------

    trend_data = (
        filtered_df.groupby("year")[
            ["heatwave", "heavy_rain", "high_wind"]
        ]
        .sum()
        .reset_index()
    )

    fig_trend = px.line(
        trend_data,
        x="year",
        y=["heatwave", "heavy_rain", "high_wind"],
        markers=True,
        title="Extreme Event Trends"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    # -------------------------
    # TOP RISK COUNTRIES
    # -------------------------

    top_risk = risk_data.sort_values(
        "risk_score", ascending=False
    ).head(10)

    colA, colB = st.columns(2)

    with colA:

        fig_bar = px.bar(
            top_risk,
            x="country",
            y="risk_score",
            title="Top 10 Climate Risk Countries",
            color="risk_score",
            color_continuous_scale="Reds"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # -------------------------
    # RISK HEATMAP
    # -------------------------

    with colB:

        heatmap_data = (
            filtered_df.groupby(["year", "month"])[
                ["heatwave", "heavy_rain", "high_wind"]
            ]
            .sum()
            .sum(axis=1)
            .reset_index(name="events")
        )

        fig_heatmap = px.density_heatmap(
            heatmap_data,
            x="month",
            y="year",
            z="events",
            color_continuous_scale="Reds",
            title="Extreme Event Heatmap"
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)