import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app import load_data, load_css, global_filters, render_kpi, section_header, make_chart_layout


def main():
    load_css()
    df = load_data()
    df_filt, _, year_range = global_filters(df)

    st.markdown(
        """
        <div class="page-title">🏳️ Regional Comparison</div>
        <div class="page-subtitle">
            Side-by-side country benchmarking across temperature, rainfall, wind, and environmental metrics.
        </div>
        <div class="accent-line"></div>
        """,
        unsafe_allow_html=True,
    )

    countries = sorted(df_filt["country"].unique().tolist())
    col_a, col_b = [st.container() for _ in range(2)]
    with col_a:
        country_a = st.selectbox("Country A", countries, key="country_a")
    with col_b:
        default_b = 1 if len(countries) > 1 else 0
        country_b = st.selectbox("Country B", countries, index=default_b, key="country_b")

    df_a = df_filt[df_filt["country"] == country_a]
    df_b = df_filt[df_filt["country"] == country_b]

    avg_temp_a = df_a["temperature_celsius"].mean()
    avg_temp_b = df_b["temperature_celsius"].mean()
    temp_diff = avg_temp_a - avg_temp_b

    rain_a = df_a["precip_mm"].mean()
    rain_b = df_b["precip_mm"].mean()
    rain_diff = rain_a - rain_b

    wind_a = df_a["wind_kph"].mean()
    wind_b = df_b["wind_kph"].mean()
    wind_diff = wind_a - wind_b

    # ---------- KPIs ----------
    section_header("📈", "Comparison Metrics")

    with st.container():

        render_kpi(
            f"{country_a} Avg Temp",
            f"{avg_temp_a:,.2f} °C" if not np.isnan(avg_temp_a) else "–",
            meta=country_a,
        )
        render_kpi(
            f"{country_b} Avg Temp",
            f"{avg_temp_b:,.2f} °C" if not np.isnan(avg_temp_b) else "–",
            meta=country_b,
        )
        render_kpi(
            "Temp Difference",
            f"{temp_diff:+.2f} °C" if not np.isnan(temp_diff) else "–",
            meta=f"{country_a} is {'warmer' if temp_diff > 0 else 'cooler'}"
            if not np.isnan(temp_diff) else None,
            meta_is_positive=bool(temp_diff > 0) if not np.isnan(temp_diff) else None,
        )
        render_kpi(
            "Rain Difference",
            f"{rain_diff:+.1f} mm" if not np.isnan(rain_diff) else "–",
            meta=f"{country_a} has {'more' if rain_diff > 0 else 'less'} rain"
            if not np.isnan(rain_diff) else None,
        )
        render_kpi(
            "Wind Difference",
            f"{wind_diff:+.1f} kph" if not np.isnan(wind_diff) else "–",
            meta=f"{country_a} has {'stronger' if wind_diff > 0 else 'weaker'} winds"
            if not np.isnan(wind_diff) else None,
        )

        # Air quality comparison if available
        if "air_quality_PM2.5" in df_filt.columns:
            pm_a = df_a["air_quality_PM2.5"].mean()
            pm_b = df_b["air_quality_PM2.5"].mean()
            pm_diff = pm_a - pm_b
            render_kpi(
                "PM2.5 Difference",
                f"{pm_diff:+.1f} µg/m³" if not np.isnan(pm_diff) else "–",
                meta=f"{country_a} has {'worse' if pm_diff > 0 else 'better'} air quality"
                if not np.isnan(pm_diff) else None,
                meta_is_positive=bool(pm_diff < 0) if not np.isnan(pm_diff) else None,
            )

        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Dual line + bar comparison ----------
    section_header("📈", "Temporal & Snapshot Comparison")

    line_col, bar_col = [st.container() for _ in range(2)]

    with line_col:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Temporal</div>'
            '<div class="panel-title">Dual Temperature Trajectory</div>',
            unsafe_allow_html=True,
        )
        comp_df = (
            df_filt[df_filt["country"].isin([country_a, country_b])]
            .groupby(["date", "country"])["temperature_celsius"]
            .mean().reset_index()
        )
        if not comp_df.empty:
            fig_dual = px.line(
                comp_df, x="date", y="temperature_celsius", color="country",
                markers=True,
                color_discrete_sequence=["#6366f1", "#f97316"],
            )
            make_chart_layout(fig_dual, height=450)
            fig_dual.update_layout(xaxis_title="Date", yaxis_title="Avg Temperature (°C)")
            st.plotly_chart(fig_dual, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No overlapping temporal data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with bar_col:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Snapshot</div>'
            '<div class="panel-title">Metric Comparison</div>',
            unsafe_allow_html=True,
        )
        bar_data = []
        for label, sub in [(country_a, df_a), (country_b, df_b)]:
            if sub.empty:
                continue
            bar_data.append(dict(
                label=label,
                avg_temp=sub["temperature_celsius"].mean(),
                avg_rain=sub["precip_mm"].mean(),
                avg_wind=sub["wind_kph"].mean(),
            ))
        bar_data = [row for row in bar_data if not np.isnan(row["avg_temp"])]
        if bar_data:
            bdf = pd.DataFrame(bar_data)
            melted = bdf.melt(id_vars="label",
                              value_vars=["avg_temp", "avg_rain", "avg_wind"],
                              var_name="metric", value_name="value")
            melted["metric"] = melted["metric"].map({
                "avg_temp": "🌡 Temp (°C)", "avg_rain": "🌧 Rain (mm)", "avg_wind": "💨 Wind (kph)"
            })
            fig_bar = px.bar(
                melted, x="metric", y="value", color="label", barmode="group",
                color_discrete_sequence=["#6366f1", "#f97316"],
            )
            make_chart_layout(fig_bar, height=450)
            fig_bar.update_layout(xaxis_title="", yaxis_title="Value", legend_title="Country")
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No comparison data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Radar + Ranking ----------
    section_header("🎯", "Climate Profile & Regional Rankings")

    radar_col, ranking_col = [st.container() for _ in range(2)]

    with radar_col:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Profile</div>'
            '<div class="panel-title">Climate Profile Radar</div>',
            unsafe_allow_html=True,
        )
        metrics = []
        for label, sub in [(country_a, df_a), (country_b, df_b)]:
            if sub.empty:
                continue
            row = dict(country=label,
                       Temperature=sub["temperature_celsius"].mean(),
                       Rainfall=sub["precip_mm"].mean(),
                       Wind=sub["wind_kph"].mean())
            if "humidity" in sub.columns:
                row["Humidity"] = sub["humidity"].mean()
            if "uv_index" in sub.columns:
                row["UV Index"] = sub["uv_index"].mean()
            metrics.append(row)

        if metrics:
            mdf = pd.DataFrame(metrics)
            categories = [c for c in mdf.columns if c != "country"]

            fig_radar = go.Figure()
            colors = ["#6366f1", "#f97316"]
            for idx, (_, row) in enumerate(mdf.iterrows()):
                fig_radar.add_trace(go.Scatterpolar(
                    r=[row[c] for c in categories],
                    theta=categories,
                    fill="toself",
                    name=row["country"],
                    fillcolor=f"rgba({99 if idx == 0 else 249},{102 if idx == 0 else 115},{241 if idx == 0 else 22},0.12)",
                    line=dict(color=colors[idx % 2], width=2),
                ))
            make_chart_layout(fig_radar, height=450)
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, gridcolor="#e2e8f0"),
                    angularaxis=dict(gridcolor="#e2e8f0"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                showlegend=True,
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Not enough data for radar.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with ranking_col:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Ranking</div>'
            '<div class="panel-title">Regional Temperature Ranking (Top 15)</div>',
            unsafe_allow_html=True,
        )
        rank_df = (
            df_filt.groupby("country")["temperature_celsius"]
            .mean().reset_index()
            .sort_values("temperature_celsius", ascending=False).head(15)
        )
        if not rank_df.empty:
            # Highlight selected countries
            rank_df["highlight"] = rank_df["country"].apply(
                lambda c: "Selected" if c in [country_a, country_b] else "Other"
            )
            fig_rank = px.bar(
                rank_df, x="temperature_celsius", y="country", orientation="h",
                color="highlight",
                color_discrete_map={"Selected": "#6366f1", "Other": "#cbd5e1"},
                text_auto=".1f",
            )
            make_chart_layout(fig_rank, height=500)
            fig_rank.update_layout(
                xaxis_title="Avg Temperature (°C)", yaxis_title="",
                yaxis=dict(autorange="reversed"),
                showlegend=False,
            )
            st.plotly_chart(fig_rank, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No ranking data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []


if __name__ == "__main__":
    main()
