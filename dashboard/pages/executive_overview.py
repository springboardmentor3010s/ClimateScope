import streamlit as st
import pandas as pd
import plotly.express as px


def show_page():

    st.header("🌍 Executive Climate Overview")

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

    st.sidebar.header("🌍 Global Filters")

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

    # if checkbox checked → force all countries
    if select_all:
        countries = all_countries

    # -------------------------
    # YEAR FILTER
    # -------------------------

    min_year = int(df["year"].min())
    max_year = int(df["year"].max())

    year_range = st.sidebar.slider(
        "Select Year Range",
        min_year,
        max_year,
        (min_year, max_year)
    )

    # -------------------------
    # MONTH FILTER
    # -------------------------

    months = sorted(df["month"].unique())

    selected_months = st.sidebar.multiselect(
        "Select Months",
        months,
        default=months
    )

    # -------------------------
    # SEASON FILTER
    # -------------------------

    seasons = sorted(df["season"].unique())

    selected_seasons = st.sidebar.multiselect(
        "Select Season",
        seasons,
        default=seasons
    )
    filtered_df = df[
        (df["country"].isin(countries)) &
        (df["year"].between(year_range[0], year_range[1])) &
        (df["month"].isin(selected_months)) &
        (df["season"].isin(selected_seasons))
    ]

    st.subheader("📌 Data Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="summary-card">
        <div class="summary-title">📊 Total Records</div>
        <div class="summary-value">{len(filtered_df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="summary-card">
        <div class="summary-title">🌍 Countries Selected</div>
        <div class="summary-value">{len(countries)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="summary-card">
        <div class="summary-title">📅 Year Range</div>
        <div class="summary-value">{year_range[0]} - {year_range[1]}</div>
        </div>
        """, unsafe_allow_html=True)

    # Handle empty dataset
    if filtered_df.empty:
        st.warning("No data available for the selected filters. Please adjust the filters.")
        return

    global_df = df[
        df["year"].between(year_range[0], year_range[1])
    ]
    st.write("")

    if st.sidebar.button("🔄 Reset Filters"):
        st.session_state.clear()
        st.rerun()

    # -------------------------
    # KPI CALCULATIONS
    # -------------------------

    avg_temp = filtered_df["temperature_celsius"].mean()
    total_precip = filtered_df["precip_mm"].sum()
    avg_wind = filtered_df["wind_kph"].mean()
    avg_humidity = filtered_df["humidity"].mean()

    extreme_events = filtered_df[
        (filtered_df["temperature_celsius"] > 40) |
        (filtered_df["precip_mm"] > 100) |
        (filtered_df["wind_kph"] > 60)
    ].shape[0]

    hottest_country = (
        global_df.groupby("country")["temperature_celsius"]
        .mean()
        .idxmax()
    )

    yearly_temp = (
        filtered_df.groupby("year")["temperature_celsius"]
        .mean()
        .reset_index()
    )

    if len(yearly_temp) > 1:
        yoy_change = (
            (yearly_temp.iloc[-1]["temperature_celsius"] -
             yearly_temp.iloc[-2]["temperature_celsius"])
            / yearly_temp.iloc[-2]["temperature_celsius"]
        ) * 100
    else:
        yoy_change = 0

    # -------------------------
    # KPI GLASS CARDS
    # -------------------------

    st.subheader("📊 Key Climate Indicators")

    col1,col2,col3,col4,col5,col6 = st.columns(6)

    with col1:
        st.markdown(f"""
        <div class="glass-card temp">
        <div class="kpi-title">🌡 Avg Temperature</div>
        <div class="kpi-value" style="color:#ef4444">{avg_temp:.2f} °C</div>
        </div>
        """,unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glass-card trend">
        <div class="kpi-title">📈 Temp Change YoY</div>
        <div class="kpi-value" style="color:#f97316">{yoy_change:.2f}%</div>
        </div>
        """,unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="glass-card rain">
        <div class="kpi-title">🌧 Total Rainfall</div>
        <div class="kpi-value" style="color:#3b82f6">{total_precip:,.0f}</div>
        </div>
        """,unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="glass-card wind">
        <div class="kpi-title">💨 Avg Wind Speed</div>
        <div class="kpi-value" style="color:#10b981">{avg_wind:.2f}</div>
        </div>
        """,unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="glass-card events">
        <div class="kpi-title">🚨 Extreme Events</div>
        <div class="kpi-value" style="color:#f59e0b">{extreme_events}</div>
        </div>
        """,unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="glass-card humidity">
        <div class="kpi-title">💧 Avg Humidity</div>
        <div class="kpi-value" style="color:#2563eb">{avg_humidity:.1f}%</div>
        </div>
        """,unsafe_allow_html=True)

    st.divider()



    # -------------------------
    # GLOBAL MAP (BIG)
    # -------------------------

    st.subheader("🌍 Global Climate Map")

    metric = st.radio(
    "Climate Metric",
    ["Temperature", "Precipitation", "Wind Speed","Humidity"],
    horizontal=True
    )

    if metric == "Temperature":
        bar_color = "#FF6B6B"

    elif metric == "Precipitation":
        bar_color = "#4D96FF"

    elif metric == "Wind Speed":
        bar_color = "#2BBBAD"

    else:
        bar_color = "#7C83FD"

    # Choose metric dynamically
    if metric == "Temperature":
        value_column = "temperature_celsius"
        color_scale = "thermal"

    elif metric == "Precipitation":
        value_column = "precip_mm"
        color_scale = "Blues"

    elif metric=="Wind Speed":
        value_column = "wind_kph"
        color_scale = "Greens"
    
    else:
        value_column="humidity"
        color_scale="purples"

    ranking_column = value_column
    # Prepare map data
    map_data = (
        filtered_df.groupby("country")[value_column]
        .mean()
        .reset_index()
    )

# Create map
    fig_map = px.choropleth(
        map_data,
        locations="country",
        locationmode="country names",
        color=value_column,
        color_continuous_scale=color_scale,
        title=f"Global {metric} Distribution"
    )

    fig_map.update_layout(height=650)

    col_map, col_hotspots = st.columns([3,1])

    with col_map:
        st.plotly_chart(fig_map, use_container_width=True)

    with col_hotspots:

        st.markdown("#### 🔥 Climate Hotspots")

        hotspot_data = (
            global_df.groupby("country")[ranking_column]
            .mean()
            .sort_values(ascending=False)
            .head(5)
        )

        for i,(country,value) in enumerate(hotspot_data.items(),1):
            st.markdown(f"""
            <div class="hotspot-card">
            🔥 <b>{i}. {country}</b><br>
            {metric}: <b>{value:.2f}</b>
            </div>
            """, unsafe_allow_html=True)


    # -------------------------
    # SECOND ROW CHARTS
    # -------------------------

    trend_data = (
        filtered_df.groupby("year")
        .agg({
            "temperature_celsius":"mean",
            "precip_mm":"mean",
            "wind_kph":"mean",
            "humidity":"mean"
        })
        .reset_index()
    )

    fig_trend = px.line(
        trend_data,
        x="year",
        y=["temperature_celsius","precip_mm","wind_kph","humidity"],
        markers=True,
        title="Global Climate Trends"
    )

    fig_trend.update_layout(
        legend_title="Climate Metrics"
    )

    # -------------------------
    # SELECTED COUNTRIES RANKING
    # -------------------------

    selected_ranking = (
        filtered_df.groupby("country")[ranking_column]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_selected_rank = px.bar(
        selected_ranking,
        x=ranking_column,
        y="country",
        orientation="h",
        title=f"Ranking of Selected Countries by {metric}",
        color_discrete_sequence=[bar_color]
    )

    fig_selected_rank.update_layout(yaxis={'categoryorder':'total ascending'})

    colA, colB = st.columns([2,1])

    with colA:
        st.plotly_chart(fig_trend, use_container_width=True)

    with colB:

        st.markdown("#### 📊 Climate Insights")

        temp_trend = trend_data["temperature_celsius"].iloc[-1] - trend_data["temperature_celsius"].iloc[0]
        rain_trend = trend_data["precip_mm"].iloc[-1] - trend_data["precip_mm"].iloc[0]
        wind_trend = trend_data["wind_kph"].iloc[-1] - trend_data["wind_kph"].iloc[0]
        humidity_trend = trend_data["humidity"].iloc[-1] - trend_data["humidity"].iloc[0]

        def trend_indicator(value):
            if value > 0:
                return "▲", "insight-up"
            elif value < 0:
                return "▼", "insight-down"
            else:
                return "■", ""
            
        temp_icon, temp_class = trend_indicator(temp_trend)
        rain_icon, rain_class = trend_indicator(rain_trend)
        wind_icon, wind_class = trend_indicator(wind_trend)
        hum_icon, hum_class = trend_indicator(humidity_trend)

        st.markdown(f"""
        <div class="insight-card">
        🌡 <b>Temperature Trend</b><br>
        <span class="{temp_class}">{temp_icon} {temp_trend:.2f}°C change</span><br>
        Global temperature variation across selected years.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-card">
        🌧 <b>Precipitation Trend</b><br>
        <span class="{rain_class}">{rain_icon} {rain_trend:.2f} mm change</span><br>
        Rainfall patterns across selected years.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-card">
        💨 <b>Wind Speed Trend</b><br>
        <span class="{wind_class}">{wind_icon} {wind_trend:.2f} kph change</span><br>
        Wind speed variation across the timeline.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-card">
        💧 <b>Humidity Trend</b><br>
        <span class="{hum_class}">{hum_icon} {humidity_trend:.2f}% change</span><br>
        Humidity changes influencing climate conditions.
        </div>
        """, unsafe_allow_html=True)

    # -------------------------
    # GLOBAL TOP COUNTRIES
    # -------------------------
    

    top_countries = (
        global_df.groupby("country")[ranking_column]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_bar = px.bar(
        top_countries,
        x="country",
        y=ranking_column,
        title=f"Top 10 Countries Globally by {metric}",
        color_discrete_sequence=[bar_color]
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    # -------------------------
    # THIRD ROW
    # -------------------------

    # -------------------------
    # THIRD ROW
    # -------------------------

    st.subheader("🔎 Climate Variable Relationships")
    st.divider()

    scatter_x = st.selectbox(
        "Select X Variable",
        ["temperature_celsius", "precip_mm", "wind_kph", "humidity"]
    )

    scatter_y = st.selectbox(
        "Select Y Variable",
        ["temperature_celsius", "precip_mm", "wind_kph", "humidity"],
        index=1
    )

    scatter = px.scatter(
        filtered_df,
        x=scatter_x,
        y=scatter_y,
        color="temperature_celsius",
        size="wind_kph",
        title=f"{scatter_x.replace('_',' ').title()} vs {scatter_y.replace('_',' ').title()}",
        color_continuous_scale="thermal"
    )

    st.plotly_chart(scatter, use_container_width=True)

    # -------------------------
    # INSIGHT BOX
    # -------------------------
    st.subheader("🧠 Executive Climate Insights")
    st.divider()

    # calculate leaders
    temp_leader = global_df.groupby("country")["temperature_celsius"].mean().idxmax()
    rain_leader = global_df.groupby("country")["precip_mm"].mean().idxmax()
    wind_leader = global_df.groupby("country")["wind_kph"].mean().idxmax()
    humidity_leader = global_df.groupby("country")["humidity"].mean().idxmax()

    st.markdown(f"""
    <div class="insight-box">

    <b>Key Observations from the Selected Climate Data:</b><br><br>

    • Average temperature across the selected regions is <b>{avg_temp:.2f}°C</b>, indicating overall climatic conditions for the chosen period.<br><br>

    • <b>{temp_leader}</b> currently records the highest average temperature globally among the dataset.<br><br>

    • <b>{rain_leader}</b> experiences the highest precipitation levels, suggesting strong rainfall concentration in that region.<br><br>

    • <b>{wind_leader}</b> shows the highest wind activity, which may indicate stronger atmospheric circulation or storm systems.<br><br>

    • <b>{humidity_leader}</b> maintains the highest humidity levels, influencing precipitation and heat index conditions.<br><br>

    • A total of <b>{extreme_events}</b> extreme weather events were detected under defined climate thresholds.

    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Download Filtered Data",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_climate_data.csv",
        mime="text/csv"
    )