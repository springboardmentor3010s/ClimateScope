import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<div style="background:#2F5597;padding:25px;border-radius:10px;text-align:center;color:white">
<h1>🌍 ClimateScope Intelligence Dashboard</h1>
<p>Advanced Climate Analytics & Comparative Insights</p>
</div>
""", unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("final_weather_data.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")

    numeric_cols = [
        "temperature_celsius","humidity","wind_kph",
        "precip_mm","air_quality_PM2.5"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Country",
    df["country"].unique()
)

metric = st.sidebar.selectbox(
    "Select Metric",
    ["temperature_celsius","humidity","wind_kph","precip_mm","air_quality_PM2.5"]
)

year_range = st.sidebar.slider(
    "Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

if countries:
    filtered_df = filtered_df[filtered_df["country"].isin(countries)]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# =====================================================
# CASE 1: SINGLE COUNTRY
# =====================================================
if len(countries) == 1:

    country = countries[0]
    st.subheader(f"{country} - Deep Analytical View ({metric})")

    # KPI VALUES
    avg_val = filtered_df[metric].mean()
    max_val = filtered_df[metric].max()
    min_val = filtered_df[metric].min()
    std_val = filtered_df[metric].std()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average", round(avg_val,2))
    col2.metric("Maximum", round(max_val,2))
    col3.metric("Minimum", round(min_val,2))
    col4.metric("Std Deviation", round(std_val,2))

    st.divider()

    # BASELINE COMPARISON
    min_year, max_year = year_range
    mid_year = (min_year + max_year) // 2

    baseline_df = filtered_df[filtered_df["year"] <= mid_year]
    current_df = filtered_df[filtered_df["year"] > mid_year]

    baseline_avg = baseline_df[metric].mean()
    current_avg = current_df[metric].mean()

    if baseline_avg and not np.isnan(baseline_avg):
        percent_change = ((current_avg - baseline_avg) / baseline_avg) * 100
        st.metric(
            "Change vs Baseline (%)",
            f"{round(percent_change,2)}%",
            delta=f"{round(percent_change,2)}%"
        )

    st.divider()

    # TREND DIRECTION
    x = np.arange(len(filtered_df))
    y = filtered_df[metric].values
    slope = np.polyfit(x, y, 1)[0]

    if slope > 0:
        st.success("Trend Direction: Increasing 📈")
        insight = "The selected metric shows a consistent upward trend."
    elif slope < 0:
        st.error("Trend Direction: Decreasing 📉")
        insight = "The selected metric shows a declining pattern."
    else:
        st.info("Trend Direction: Stable ➖")
        insight = "The selected metric remains relatively stable."

    st.info(f"📌 Insight: {insight}")

    st.divider()

    # Z-SCORE OUTLIERS
    if std_val and not np.isnan(std_val):
        z = (filtered_df[metric] - avg_val) / std_val
        extremes = filtered_df[abs(z) > 2]
        st.write("Statistical Outliers (|Z| > 2):", len(extremes))

    st.divider()

    # TREND WITH MOVING AVERAGE
    st.subheader("Trend Over Time (Smoothed)")

    filtered_df = filtered_df.sort_values("last_updated")
    filtered_df["Moving_Avg"] = filtered_df[metric].rolling(window=5).mean()

    fig1 = px.line(
        filtered_df,
        x="last_updated",
        y=[metric, "Moving_Avg"]
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # SCATTER
    st.subheader("Metric vs Wind Relationship")

    fig2 = px.scatter(
        filtered_df,
        x="wind_kph",
        y=metric,
        color="year"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # CORRELATION
    st.subheader("Correlation Heatmap")

    corr = filtered_df[
        ["temperature_celsius","humidity","wind_kph",
         "precip_mm","air_quality_PM2.5"]
    ].corr()

    fig3 = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu")
    st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# CASE 2: MULTIPLE COUNTRIES
# =====================================================
elif len(countries) > 1:

    st.subheader("Comparative & Collaborative Analysis")

    avg_map = filtered_df.groupby("country")[metric].mean().reset_index()

    fig_map = px.choropleth(
        avg_map,
        locations="country",
        locationmode="country names",
        color=metric,
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.divider()

    ranking = avg_map.sort_values(metric, ascending=False)
    st.write("Country Ranking:")
    st.dataframe(ranking)

    st.success(f"Highest {metric}: {ranking.iloc[0]['country']}")
    st.warning(f"Lowest {metric}: {ranking.iloc[-1]['country']}")

    st.divider()

    st.subheader("Trend Comparison")

    fig_line = px.line(
        filtered_df.sort_values("last_updated"),
        x="last_updated",
        y=metric,
        color="country"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.divider()

    st.subheader("Scatter Comparison")

    fig_scatter = px.scatter(
        filtered_df,
        x="wind_kph",
        y=metric,
        color="country"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    st.subheader("Mean Comparison Heatmap")

    mean_matrix = filtered_df.groupby("country")[
        ["temperature_celsius","humidity","wind_kph",
         "precip_mm","air_quality_PM2.5"]
    ].mean()

    fig_heat = px.imshow(mean_matrix, text_auto=True, color_continuous_scale="RdBu")
    st.plotly_chart(fig_heat, use_container_width=True)

# =====================================================
# CASE 3: GLOBAL VIEW
# =====================================================
else:

    st.subheader("Global Overview")

    avg_global = filtered_df.groupby("country")[metric].mean().reset_index()

    fig_global = px.choropleth(
        avg_global,
        locations="country",
        locationmode="country names",
        color=metric,
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig_global, use_container_width=True)