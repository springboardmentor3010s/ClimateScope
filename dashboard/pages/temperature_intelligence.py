import streamlit as st
import pandas as pd
import plotly.express as px


def show_page():

    st.header("🌡 Temperature Intelligence")

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

    st.sidebar.header("Temperature Filters")

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

    avg_temp = filtered_df["temperature_celsius"].mean()

    max_temp = filtered_df["temperature_celsius"].max()

    min_temp = filtered_df["temperature_celsius"].min()

    temp_std = filtered_df["temperature_celsius"].std()

    yearly_temp = (
        filtered_df.groupby("year")["temperature_celsius"]
        .mean()
        .reset_index()
    )


    if len(yearly_temp) > 1:
        trend = (
            yearly_temp.iloc[-1]["temperature_celsius"] -
            yearly_temp.iloc[0]["temperature_celsius"]
        )
    else:
        trend = 0

    # -------------------------
    # KPI CARDS
    # -------------------------

    st.subheader("Temperature Indicators")

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.metric("Avg Temperature", f"{avg_temp:.2f} °C")

    with col2:
        st.metric("Max Temperature", f"{max_temp:.2f} °C")

    with col3:
        st.metric("Min Temperature", f"{min_temp:.2f} °C")

    with col4:
        st.metric("Temperature Variability", f"{temp_std:.2f}")

    with col5:
        st.metric("Temperature Trend", f"{trend:.2f} °C")

    st.divider()

    # -------------------------
    # TEMPERATURE TREND
    # -------------------------

    st.subheader("Temperature Trend Over Time")

    fig_trend = px.line(
        yearly_temp,
        x="year",
        y="temperature_celsius",
        markers=True,
        title="Average Temperature by Year"
    )

    st.plotly_chart(fig_trend, use_container_width=True)


    # -------------------------
    # TEMPERATURE ANOMALY
    # -------------------------

    st.subheader("Temperature Anomaly")

    baseline = filtered_df["temperature_celsius"].mean()

    yearly_temp["anomaly"] = yearly_temp["temperature_celsius"] - baseline

    fig_anomaly = px.bar(
        yearly_temp,
        x="year",
        y="anomaly",
        color="anomaly",
        color_continuous_scale=["blue","white","red"],
        title="Temperature Anomaly Relative to Average"
    )

    st.plotly_chart(fig_anomaly, use_container_width=True)


    # -------------------------
    # SEASONAL HEATMAP
    # -------------------------

    st.subheader("Seasonal Temperature Heatmap")

    filtered_df["month_name"] = pd.to_datetime(filtered_df["month"], format="%m").dt.strftime("%b")


    heatmap_data = filtered_df.pivot_table(
        values="temperature_celsius",
        index="year",
        columns="month",
        aggfunc="mean"
    )

    fig_heatmap = px.imshow(
        heatmap_data,
        color_continuous_scale="thermal",
        labels=dict(
            x="Month",
            y="Year",
            color="Temperature (°C)"
        ),
        title="Seasonal Temperature Patterns"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)


    

    st.subheader("🌍 Country Temperature Comparison")
    st.divider()

    compare_countries = st.multiselect(
        "Select Countries to Compare",
        sorted(filtered_df["country"].unique()),
        default=[]
    )

    # if nothing selected → show all countries
    if not compare_countries:
        compare_countries = sorted(filtered_df["country"].unique())

    comparison_data = (
        filtered_df[filtered_df["country"].isin(compare_countries)]
        .groupby(["year", "country"])["temperature_celsius"]
        .mean()
        .reset_index()
    )

    fig_compare = px.line(
        comparison_data,
        x="year",
        y="temperature_celsius",
        color="country",
        markers=True,
        title="Temperature Trends for Selected Countries"
    )

    st.plotly_chart(fig_compare, use_container_width=True)



    # -------------------------
    # DISTRIBUTION + COUNTRY COMPARISON
    # -------------------------

    colA,colB = st.columns(2)

    with colA:

        st.subheader("Temperature Distribution")

        fig_hist = px.histogram(
            filtered_df,
            x="temperature_celsius",
            nbins=40,
            title="Temperature Distribution"
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    with colB:

        country_temp = (
            filtered_df.groupby("country")["temperature_celsius"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig_box = px.box(
        filtered_df,
        x="country",
        y="temperature_celsius",
        color="country",
        title="Temperature Distribution by Country"
    )

    st.plotly_chart(fig_box, use_container_width=True)
