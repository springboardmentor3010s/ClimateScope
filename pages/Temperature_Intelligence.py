from datetime import datetime
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app import load_data, load_css, global_filters, render_kpi, section_header, make_chart_layout


def main():
    load_css()
    df = load_data()
    df_filt, country_sel, year_range = global_filters(df)

    st.markdown(
        """
        <div class="page-title">🌡️ Temperature Intelligence</div>
        <div class="page-subtitle">
            Deep dive into temperature levels, anomalies, seasonal dynamics, and heat stress.
        </div>
        <div class="accent-line"></div>
        """,
        unsafe_allow_html=True,
    )

    current = df_filt.copy()
    current_avg = current["temperature_celsius"].mean()
    max_temp = current["temperature_celsius"].max()
    min_temp = current["temperature_celsius"].min()
    temp_std = current["temperature_celsius"].std()

    # Anomaly calculation
    if country_sel != "All":
        baseline = df.groupby("country")["temperature_celsius"].mean()
        base_val = baseline.get(country_sel, np.nan)
        temp_anomaly = current_avg - base_val
    else:
        baseline_global = df["temperature_celsius"].mean()
        temp_anomaly = current_avg - baseline_global

    # Feels-like comparison
    has_feels_like = "feels_like_celsius" in current.columns
    avg_feels_like = current["feels_like_celsius"].mean() if has_feels_like else np.nan
    heat_stress = avg_feels_like - current_avg if has_feels_like else np.nan

    # ---------- KPIs ----------
    section_header("📈", "Temperature Metrics")

    with st.container():

        render_kpi(
            "Current Avg Temperature",
            f"{current_avg:,.2f} °C" if not np.isnan(current_avg) else "–",
            meta=f"Period {year_range[0]}–{year_range[1]}",
        )
        render_kpi(
            "Max Temperature",
            f"{max_temp:,.2f} °C" if not np.isnan(max_temp) else "–",
            meta="Peak recorded",
            meta_is_positive=False,
        )
        render_kpi(
            "Min Temperature",
            f"{min_temp:,.2f} °C" if not np.isnan(min_temp) else "–",
            meta="Lowest recorded",
        )
        render_kpi(
            "Temperature Anomaly",
            f"{temp_anomaly:+.2f} °C" if not np.isnan(temp_anomaly) else "–",
            meta=f"{'▲' if temp_anomaly > 0 else '▼'} {temp_anomaly:+.2f} °C vs baseline"
            if not np.isnan(temp_anomaly) else None,
            meta_is_positive=bool(temp_anomaly > 0) if not np.isnan(temp_anomaly) else None,
        )
        render_kpi(
            "Temp Variability",
            f"{temp_std:,.2f} °C" if not np.isnan(temp_std) else "–",
            meta="Standard deviation",
        )
        if has_feels_like:
            render_kpi(
                "Feels Like Avg",
                f"{avg_feels_like:,.2f} °C" if not np.isnan(avg_feels_like) else "–",
                meta=f"Heat stress: {heat_stress:+.2f} °C" if not np.isnan(heat_stress) else None,
                meta_is_positive=bool(heat_stress <= 0) if not np.isnan(heat_stress) else None,
            )

        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Charts ----------
    section_header("📈", "Temporal & Seasonal Patterns")

    top_left, top_right = [st.container() for _ in range(2)]

    with top_left:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Temporal</div>'
            '<div class="panel-title">Monthly Temperature Trend</div>',
            unsafe_allow_html=True,
        )
        if not df_filt.empty:
            ts_df = df_filt.groupby("date")["temperature_celsius"].mean().reset_index()
            fig_ts = px.area(
                ts_df, x="date", y="temperature_celsius",
                color_discrete_sequence=["#6366f1"],
            )
            make_chart_layout(fig_ts, height=450)
            fig_ts.update_traces(
                line=dict(width=3, color="#6366f1"),
                fillcolor="rgba(99,102,241,0.08)",
                hovertemplate="%{x|%b %Y}<br>Avg Temp: %{y:.2f} °C<extra></extra>",
            )
            fig_ts.update_layout(xaxis_title="Date", yaxis_title="Temperature (°C)")
            st.plotly_chart(fig_ts, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No time series data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with top_right:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Seasonality</div>'
            '<div class="panel-title">Seasonal Temperature Heatmap</div>',
            unsafe_allow_html=True,
        )
        if not df_filt.empty:
            season_df = df_filt.groupby(["year", "month"])["temperature_celsius"].mean().reset_index()
            month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                           7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
            pivot = season_df.pivot(index="year", columns="month", values="temperature_celsius").sort_index()
            pivot = pivot.rename(columns=month_names)

            fig_hm = px.imshow(
                pivot,
                color_continuous_scale=["#dbeafe", "#6366f1", "#dc2626"],
                aspect="auto",
            )
            make_chart_layout(fig_hm, height=450)
            fig_hm.update_layout(xaxis_title="Month", yaxis_title="Year")
            st.plotly_chart(fig_hm, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No seasonal data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Distribution + Comparison ----------
    section_header("📈", "Distribution & Country Comparison")

    bottom_left, bottom_right = [st.container() for _ in range(2)]

    with bottom_left:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Distribution</div>'
            '<div class="panel-title">Temperature Distribution</div>',
            unsafe_allow_html=True,
        )
        if not df_filt.empty:
            fig_hist = px.histogram(
                df_filt, x="temperature_celsius", nbins=40,
                marginal="box",
                color_discrete_sequence=["#6366f1"],
            )
            make_chart_layout(fig_hist, height=450)
            fig_hist.update_layout(xaxis_title="Temperature (°C)", yaxis_title="Count")
            st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No distribution data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with bottom_right:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Benchmarking</div>'
            '<div class="panel-title">Multi-Country Temperature Comparison</div>',
            unsafe_allow_html=True,
        )
        countries = sorted(df_filt["country"].unique().tolist())
        selected = st.multiselect(
            "Select countries to compare",
            countries,
            default=countries[:min(4, len(countries))],
        )
        if selected:
            comp_df = df_filt[df_filt["country"].isin(selected)]
            comp_ts = comp_df.groupby(["date", "country"])["temperature_celsius"].mean().reset_index()
            fig_cmp = px.line(
                comp_ts, x="date", y="temperature_celsius", color="country",
                markers=True,
            )
            make_chart_layout(fig_cmp, height=450)
            fig_cmp.update_layout(xaxis_title="Date", yaxis_title="Avg Temperature (°C)")
            st.plotly_chart(fig_cmp, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Select at least one country to compare.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Feels-Like Comparison ----------
    if has_feels_like:
        section_header("🌡", "Heat Stress Analysis")

        fl_col1, fl_col2 = [st.container() for _ in range(2)]

        with fl_col1:
            st.markdown(
                '<div class="glass-panel"><div class="panel-header">Comparison</div>'
                '<div class="panel-title">Actual vs Feels-Like Temperature</div>',
                unsafe_allow_html=True,
            )
            fl_df = df_filt.groupby("date").agg(
                actual=("temperature_celsius", "mean"),
                feels_like=("feels_like_celsius", "mean"),
            ).reset_index()
            if not fl_df.empty:
                fig_fl = go.Figure()
                fig_fl.add_trace(go.Scatter(
                    x=fl_df["date"], y=fl_df["actual"], name="Actual",
                    line=dict(color="#6366f1", width=2),
                ))
                fig_fl.add_trace(go.Scatter(
                    x=fl_df["date"], y=fl_df["feels_like"], name="Feels Like",
                    line=dict(color="#f97316", width=2, dash="dash"),
                ))
                make_chart_layout(fig_fl, height=450)
                fig_fl.update_layout(xaxis_title="Date", yaxis_title="Temperature (°C)")
                st.plotly_chart(fig_fl, use_container_width=True, config={"displayModeBar": False})
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

        with fl_col2:
            st.markdown(
                '<div class="glass-panel"><div class="panel-header">Heat Stress</div>'
                '<div class="panel-title">Heat Stress by Country (Top 10)</div>',
                unsafe_allow_html=True,
            )
            hs_df = df_filt.copy()
            hs_df["heat_stress"] = hs_df["feels_like_celsius"] - hs_df["temperature_celsius"]
            hs_country = hs_df.groupby("country")["heat_stress"].mean().reset_index()
            hs_top = hs_country.sort_values("heat_stress", ascending=False).head(10)
            if not hs_top.empty:
                fig_hs = px.bar(
                    hs_top, x="heat_stress", y="country", orientation="h",
                    text_auto=".2f",
                    color="heat_stress",
                    color_continuous_scale=["#d1fae5", "#f59e0b", "#dc2626"],
                )
                make_chart_layout(fig_hs, height=450)
                fig_hs.update_layout(
                    coloraxis_showscale=False,
                    xaxis_title="Heat Stress (°C)", yaxis_title="",
                    yaxis=dict(autorange="reversed"),
                )
                st.plotly_chart(fig_hs, use_container_width=True, config={"displayModeBar": False})
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []


if __name__ == "__main__":
    main()
