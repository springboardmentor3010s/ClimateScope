import numpy as np
import plotly.express as px
import streamlit as st

from app import load_data, load_css, global_filters, render_kpi, section_header, make_chart_layout, get_map_colors


def categorize_risk(score: float) -> str:
    if np.isnan(score):
        return "N/A"
    if score < 30:
        return "Low"
    if score < 60:
        return "Medium"
    return "High"


def risk_badge_class(cat: str) -> str:
    return {"Low": "stat-badge-green", "Medium": "stat-badge-amber", "High": "stat-badge-red"}.get(cat, "stat-badge-blue")


def main():
    load_css()
    df = load_data()
    df_filt, country_sel, year_range = global_filters(df)

    st.markdown(
        """
        <div class="page-title">⚠️ Climate Risk Intelligence</div>
        <div class="page-subtitle">
            Composite climate risk scores, categories, volatility analytics, and air quality risk factors.
        </div>
        <div class="accent-line"></div>
        """,
        unsafe_allow_html=True,
    )

    risk = df_filt.copy()
    if "risk_score" not in risk.columns:
        risk["risk_score"] = (
            risk["temperature_celsius"] * 0.4
            + risk["precip_mm"] * 0.3
            + risk["wind_kph"] * 0.3
        )

    avg_risk = risk["risk_score"].mean()
    volatility = risk["risk_score"].std()

    first_year = risk["year"].min()
    last_year = risk["year"].max()
    start_risk = risk[risk["year"] == first_year]["risk_score"].mean()
    end_risk = risk[risk["year"] == last_year]["risk_score"].mean()
    trend_direction = "Upward" if end_risk > start_risk else "Downward"
    trend_pct = (end_risk - start_risk) / start_risk * 100 if start_risk else np.nan

    risk_category = categorize_risk(avg_risk)

    # Air quality risk component
    has_pm25 = "air_quality_PM2.5" in risk.columns
    avg_pm25 = risk["air_quality_PM2.5"].mean() if has_pm25 else np.nan
    has_ozone = "air_quality_Ozone" in risk.columns
    avg_ozone = risk["air_quality_Ozone"].mean() if has_ozone else np.nan

    # ---------- KPIs ----------
    section_header("📈", "Risk Metrics")

    with st.container():

        render_kpi(
            "Climate Risk Score",
            f"{avg_risk:,.1f}" if not np.isnan(avg_risk) else "–",
            meta=f"{risk_category} risk",
            meta_is_positive=bool(avg_risk < 30) if not np.isnan(avg_risk) else None,
        )
        render_kpi(
            "Risk Category",
            risk_category,
            meta=f"Based on composite score of {avg_risk:.1f}" if not np.isnan(avg_risk) else None,
            meta_is_positive=bool(avg_risk < 30) if not np.isnan(avg_risk) else None,
        )
        render_kpi(
            "Volatility Index",
            f"{volatility:,.1f}" if not np.isnan(volatility) else "–",
            meta="Higher = more variability",
            meta_is_positive=bool(volatility < 15) if not np.isnan(volatility) else None,
        )
        render_kpi(
            "Trend Direction",
            trend_direction if not np.isnan(trend_pct) else "–",
            meta=f"{trend_pct:+.1f}% over period" if not np.isnan(trend_pct) else None,
            meta_is_positive=bool(trend_pct < 0) if not np.isnan(trend_pct) else None,
        )
        if has_pm25:
            pm25_cat = "Good" if avg_pm25 < 35 else "Unhealthy"
            render_kpi(
                "Air Quality (PM2.5)",
                f"{avg_pm25:,.1f} µg/m³" if not np.isnan(avg_pm25) else "–",
                meta=pm25_cat,
                meta_is_positive=bool(avg_pm25 < 35) if not np.isnan(avg_pm25) else None,
            )
        if has_ozone:
            render_kpi(
                "Ozone Level",
                f"{avg_ozone:,.1f} µg/m³" if not np.isnan(avg_ozone) else "–",
                meta="Avg ground-level ozone",
            )

        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # Risk status badge
    badge_cls = risk_badge_class(risk_category)
    st.markdown(
        f"""
        <div style="display:flex; gap:0.5rem; margin-bottom:1rem; flex-wrap:wrap;">
            <span class="stat-badge {badge_cls}">Overall Risk: {risk_category}</span>
            <span class="stat-badge stat-badge-purple">Volatility: {volatility:.1f}</span>
            <span class="stat-badge stat-badge-blue">Trend: {trend_direction}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Maps & Rankings ----------
    section_header("🗺", "Spatial Risk Analysis")

    top_left, top_right = [st.container() for _ in range(2)]

    with top_left:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Spatial</div>'
            '<div class="panel-title">Risk Score by Country</div>',
            unsafe_allow_html=True,
        )
        if not risk.empty:
            by_country = risk.groupby("country")["risk_score"].mean().reset_index()
            fig_country = px.choropleth(
                by_country, locations="country", locationmode="country names",
                color="risk_score",
                color_continuous_scale=["#d1fae5", "#fde68a", "#fecaca", "#dc2626"],
            )
            make_chart_layout(fig_country, height=450)
            map_colors = get_map_colors()
            fig_country.update_layout(
                coloraxis_colorbar=dict(title="Risk Score"),
                geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False,
                         showcoastlines=True, coastlinecolor=map_colors["coastlinecolor"],
                         landcolor=map_colors["landcolor"], lakecolor=map_colors["lakecolor"]),
            )
            st.plotly_chart(fig_country, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No risk data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with top_right:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Ranking</div>'
            '<div class="panel-title">Top 10 Risk Countries</div>',
            unsafe_allow_html=True,
        )
        if not risk.empty:
            top10 = (
                risk.groupby("country")["risk_score"].mean().reset_index()
                .sort_values("risk_score", ascending=False).head(10)
            )
            fig_top = px.bar(
                top10, x="risk_score", y="country", orientation="h",
                text_auto=".1f", color="risk_score",
                color_continuous_scale=["#fde68a", "#f97316", "#dc2626"],
            )
            make_chart_layout(fig_top, height=450)
            fig_top.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Avg Risk Score", yaxis_title="",
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig_top, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No ranking available.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Trend & Heatmap ----------
    section_header("📈", "Risk Trends & Seasonality")

    bottom_left, bottom_right = [st.container() for _ in range(2)]

    with bottom_left:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Temporal</div>'
            '<div class="panel-title">Risk Trend Over Time</div>',
            unsafe_allow_html=True,
        )
        if not risk.empty:
            trend_df = risk.groupby("date")["risk_score"].mean().reset_index()
            fig_trend = px.area(
                trend_df, x="date", y="risk_score",
                color_discrete_sequence=["#f59e0b"],
            )
            make_chart_layout(fig_trend, height=450)
            fig_trend.update_traces(
                line=dict(width=3, color="#f59e0b"),
                fillcolor="rgba(245,158,11,0.08)",
                hovertemplate="%{x|%b %Y}<br>Risk Score: %{y:.1f}<extra></extra>",
            )
            fig_trend.update_layout(xaxis_title="Date", yaxis_title="Risk Score")
            st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No trend data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with bottom_right:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Seasonality</div>'
            '<div class="panel-title">Risk Heatmap (Year × Month)</div>',
            unsafe_allow_html=True,
        )
        if not risk.empty:
            hm = risk.groupby(["year", "month"])["risk_score"].mean().reset_index()
            month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                           7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
            pivot = hm.pivot(index="year", columns="month", values="risk_score")
            pivot = pivot.rename(columns=month_names)
            fig_hm = px.imshow(
                pivot,
                color_continuous_scale=["#ede9fe", "#8b5cf6", "#4c1d95"],
                aspect="auto",
            )
            make_chart_layout(fig_hm, height=450)
            fig_hm.update_layout(xaxis_title="Month", yaxis_title="Year")
            st.plotly_chart(fig_hm, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No heatmap data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Air Quality Section ----------
    if has_pm25:
        section_header("🏭", "Air Quality Risk Factors")

        aq_col1, aq_col2 = [st.container() for _ in range(2)]

        with aq_col1:
            st.markdown(
                '<div class="glass-panel"><div class="panel-header">Trend</div>'
                '<div class="panel-title">PM2.5 Trend Over Time</div>',
                unsafe_allow_html=True,
            )
            pm_ts = risk.groupby("date")["air_quality_PM2.5"].mean().reset_index()
            if not pm_ts.empty:
                fig_pm = px.area(
                    pm_ts, x="date", y="air_quality_PM2.5",
                    color_discrete_sequence=["#ef4444"],
                )
                make_chart_layout(fig_pm, height=450)
                fig_pm.update_traces(
                    line=dict(width=2, color="#ef4444"),
                    fillcolor="rgba(239,68,68,0.06)",
                )
                fig_pm.update_layout(xaxis_title="Date", yaxis_title="PM2.5 (µg/m³)")
                st.plotly_chart(fig_pm, use_container_width=True, config={"displayModeBar": False})
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

        with aq_col2:
            st.markdown(
                '<div class="glass-panel"><div class="panel-header">Distribution</div>'
                '<div class="panel-title">PM2.5 Distribution</div>',
                unsafe_allow_html=True,
            )
            fig_pmd = px.histogram(
                risk, x="air_quality_PM2.5", nbins=40,
                color_discrete_sequence=["#f97316"],
            )
            make_chart_layout(fig_pmd, height=450)
            fig_pmd.update_layout(xaxis_title="PM2.5 (µg/m³)", yaxis_title="Count")
            st.plotly_chart(fig_pmd, use_container_width=True, config={"displayModeBar": False})
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []


if __name__ == "__main__":
    main()
