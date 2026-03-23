import streamlit as st
import plotly.express as px

from utils import CLIMATE_CONTINUOUS, CLIMATE_PALETTE


def render(df, selected_country="All", selected_year="All"):
    st.title("⚠ Climate Risk Intelligence")
    st.write("This page estimates climate risk using multiple environmental indicators.")

    filtered = df.copy()
    if selected_country != "All":
        filtered = filtered[filtered["country"] == selected_country]
    if selected_year != "All":
        filtered = filtered[filtered["year"] == selected_year]

    # Risk Score
    filtered["risk_score"] = (
        filtered["temperature_celsius"] * 0.5
        + filtered["wind_kph"] * 0.3
        + filtered["precip_mm"] * 0.2
    )

    risk_mean = filtered["risk_score"].mean()

    # Volatility
    volatility = filtered["risk_score"].std()

    # Trend
    trend = filtered.groupby("year")["risk_score"].mean()
    trend_dir = "▲ Increasing" if len(trend) > 1 and trend.iloc[-1] > trend.iloc[0] else "▼ Decreasing"

    # Category
    if risk_mean < 30:
        category = "Low"
    elif risk_mean < 60:
        category = "Moderate"
    else:
        category = "High"

    # KPIs
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Climate Risk Score", round(risk_mean, 2))
    c2.metric("Risk Category", category)
    c3.metric("Volatility Index", round(volatility, 2))
    c4.metric("Trend Direction", trend_dir)

    # Risk by Country
    st.subheader("Risk Score by Country")
    risk_country = filtered.groupby("country")["risk_score"].mean().reset_index()

    fig = px.bar(
        risk_country,
        x="country",
        y="risk_score",
        color_discrete_sequence=CLIMATE_PALETTE,
    )
    st.plotly_chart(fig, width="stretch", key="cri_risk_by_country")

    st.info("Insight: Countries with higher risk scores experience stronger climate stress.")

    # Risk Trend
    st.subheader("Risk Trend Over Time")
    trend_df = trend.reset_index()

    fig2 = px.line(
        trend_df,
        x="year",
        y="risk_score",
        color_discrete_sequence=CLIMATE_PALETTE,
    )
    st.plotly_chart(fig2, width="stretch", key="cri_risk_trend")

    st.info("Insight: Increasing risk trends highlight worsening climate conditions.")

    # Risk Heatmap
    st.subheader("Risk Heatmap")
    heat = filtered.pivot_table(values="risk_score", index="year", columns="month")

    fig3 = px.imshow(
        heat,
        width=700,
        color_continuous_scale=CLIMATE_CONTINUOUS,
    )
    st.plotly_chart(fig3, width="stretch", key="cri_heatmap")

    st.info("Insight: The heatmap highlights periods of elevated climate risk.")

    # Top Risk Countries
    st.subheader("Top 10 Risk Countries")

    # Compute rankings across all countries for the selected year (or full range)
    ranking_df = df.copy()
    if selected_year != "All":
        ranking_df = ranking_df[ranking_df["year"] == selected_year]

    ranking_df["risk_score"] = (
        ranking_df["temperature_celsius"] * 0.5
        + ranking_df["wind_kph"] * 0.3
        + ranking_df["precip_mm"] * 0.2
    )

    ranking_by_country = (
        ranking_df.groupby("country")["risk_score"].mean().reset_index().sort_values("risk_score", ascending=False)
    )
    ranking_by_country = ranking_by_country.reset_index(drop=True)
    ranking_by_country["rank"] = ranking_by_country.index + 1

    selected_rank = None
    if selected_country != "All":
        sel = ranking_by_country[ranking_by_country["country"] == selected_country]
        if not sel.empty:
            selected_rank = int(sel["rank"].iloc[0])

    top = ranking_by_country.head(10)

    fig4 = px.bar(
        top,
        x="country",
        y="risk_score",
        color_discrete_sequence=CLIMATE_PALETTE,
    )
    st.plotly_chart(fig4, width="stretch", key="cri_top10")

    if selected_country != "All" and selected_rank is not None:
        total = len(ranking_by_country)
        st.info(
            f"Insight: {selected_country} ranks #{selected_rank} out of {total} countries by risk score for the selected period."
        )
    elif selected_country != "All":
        st.info(
            "Insight: No ranking available for the selected country (check your filters or data availability)."
        )
    else:
        st.info("Insight: These countries require stronger climate adaptation strategies.")

    st.markdown(
        "<div style='text-align:center; margin-top:2rem; font-size:0.9rem; color:rgba(255,255,255,0.8);'>"
        "<a href='#top' style='color:#80d4ff; text-decoration:none;'>⬆ Back to top</a>"
        "</div>",
        unsafe_allow_html=True,
    )
