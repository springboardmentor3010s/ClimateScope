import numpy as np
import plotly.express as px
import streamlit as st

from app import load_data, load_css, global_filters, render_kpi, section_header, make_chart_layout, get_map_colors


def main():
    load_css()
    df = load_data()
    df_filt, country_sel, year_range = global_filters(df)

    st.markdown(
        """
        <div class="page-title">📋 Executive Overview</div>
        <div class="page-subtitle">
            High-level global climate signals for leadership and decision-makers.
        </div>
        <div class="accent-line"></div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- KPIs ----------
    latest_year = df_filt["year"].max()
    prev_year = latest_year - 1
    current = df_filt[df_filt["year"] == latest_year]
    prev = df_filt[df_filt["year"] == prev_year]

    global_avg_temp = current["temperature_celsius"].mean()
    prev_avg_temp = prev["temperature_celsius"].mean() if not prev.empty else np.nan
    yoy_temp_change = (
        (global_avg_temp - prev_avg_temp) / prev_avg_temp * 100
        if not np.isnan(prev_avg_temp) and prev_avg_temp != 0
        else np.nan
    )

    total_precip = current["precip_mm"].sum()
    avg_wind = current["wind_kph"].mean()
    extreme_events = int(current["has_extreme_event"].sum())
    avg_humidity = current["humidity"].mean() if "humidity" in current.columns else np.nan
    avg_uv = current["uv_index"].mean() if "uv_index" in current.columns else np.nan

    hottest_country = (
        current.groupby("country")["temperature_celsius"].mean().idxmax()
        if not current.empty
        else "N/A"
    )

    section_header("📈", "Key Metrics")

    with st.container():

        render_kpi(
            "Global Avg Temperature",
            f"{global_avg_temp:,.2f} °C" if not np.isnan(global_avg_temp) else "–",
            meta=f"Year {latest_year}",
            meta_is_positive=bool(yoy_temp_change > 0) if not np.isnan(yoy_temp_change) else None,
        )
        render_kpi(
            "Temperature YoY Change",
            f"{yoy_temp_change:+.1f} %" if not np.isnan(yoy_temp_change) else "–",
            meta="vs previous year",
            meta_is_positive=bool(yoy_temp_change > 0) if not np.isnan(yoy_temp_change) else None,
        )
        render_kpi(
            "Total Precipitation",
            f"{total_precip:,.0f} mm" if not np.isnan(total_precip) else "–",
            meta=f"{latest_year}",
        )
        render_kpi(
            "Average Wind Speed",
            f"{avg_wind:,.1f} kph" if not np.isnan(avg_wind) else "–",
            meta=f"{latest_year}",
        )
        render_kpi(
            "Extreme Events Count",
            f"{extreme_events:,}",
            meta=f"{latest_year}",
            meta_is_positive=bool(extreme_events < 50),
        )
        render_kpi("Hottest Country", hottest_country, meta=f"{latest_year}")

        if not np.isnan(avg_humidity):
            render_kpi("Avg Humidity", f"{avg_humidity:.1f}%", meta=f"{latest_year}")
        if not np.isnan(avg_uv):
            render_kpi("Avg UV Index", f"{avg_uv:.1f}", meta=f"{latest_year}",
                       meta_is_positive=bool(avg_uv <= 6))

        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Map + Trend ----------
    section_header("🗺", "Geospatial & Temporal Analysis")

    map_col, trend_col = [st.container() for _ in range(2)]

    with map_col:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Geospatial</div>'
            '<div class="panel-title">Global Temperature Choropleth</div>'
            '<div class="panel-subtitle">Average surface temperature by country.</div>',
            unsafe_allow_html=True,
        )
        if not current.empty:
            map_df = current.groupby("country")["temperature_celsius"].mean().reset_index()
            fig_map = px.choropleth(
                map_df, locations="country", locationmode="country names",
                color="temperature_celsius", color_continuous_scale="Turbo",
            )
            make_chart_layout(fig_map, height=450)
            map_colors = get_map_colors()
            fig_map.update_layout(
                coloraxis_colorbar=dict(title="°C"),
                geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False,
                         showcoastlines=True, coastlinecolor=map_colors["coastlinecolor"],
                         landcolor=map_colors["landcolor"], lakecolor=map_colors["lakecolor"]),
            )
            fig_map.update_traces(
                hovertemplate="<b>%{location}</b><br>Avg Temp: %{z:.2f} °C<extra></extra>"
            )
            st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No data available for the selected filters.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with trend_col:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Temporal</div>'
            '<div class="panel-title">Global Temperature Trend</div>'
            '<div class="panel-subtitle">Multi-year evolution of global average temperature.</div>',
            unsafe_allow_html=True,
        )
        trend_df = df_filt.groupby("date")["temperature_celsius"].mean().reset_index()
        if not trend_df.empty:
            fig_trend = px.area(
                trend_df, x="date", y="temperature_celsius",
                color_discrete_sequence=["#6366f1"],
            )
            make_chart_layout(fig_trend, height=450)
            fig_trend.update_traces(
                line=dict(width=3, color="#6366f1"),
                fillcolor="rgba(99,102,241,0.08)",
                hovertemplate="%{x|%b %Y}<br>Global Avg: %{y:.2f} °C<extra></extra>",
            )
            fig_trend.update_layout(xaxis_title="Date", yaxis_title="Avg Temperature (°C)")
            st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No temporal data for the selected filters.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Top 5 + Executive Insight ----------
    section_header("📝", "Rankings & Executive Insights")

    bottom_left, bottom_right = [st.container() for _ in range(2)]

    with bottom_left:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Ranking</div>'
            '<div class="panel-title">Top 5 Hottest Countries</div>',
            unsafe_allow_html=True,
        )
        if not current.empty:
            top5 = (
                current.groupby("country")["temperature_celsius"]
                .mean().reset_index()
                .sort_values("temperature_celsius", ascending=False).head(5)
            )
            fig_bar = px.bar(
                top5, x="temperature_celsius", y="country", orientation="h",
                text_auto=".2f", color="temperature_celsius",
                color_continuous_scale=["#fde68a", "#f97316", "#dc2626"],
            )
            make_chart_layout(fig_bar, height=450)
            fig_bar.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Avg Temperature (°C)", yaxis_title="",
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No ranking available.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with bottom_right:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Narrative</div>'
            '<div class="panel-title">Executive Insight Summary</div>',
            unsafe_allow_html=True,
        )
        if not current.empty:
            risk_hotspot = (
                current.groupby("country")["risk_score"].mean().idxmax()
                if "risk_score" in current.columns and not current.empty
                else hottest_country
            )
            risk_level = "🟢 Low" if extreme_events < 20 else ("🟡 Medium" if extreme_events < 100 else "🔴 High")

            st.markdown(
                f"""
                <p style="font-size:0.88rem; color:#334155; line-height:1.7;">
                    Over the selected period, global average temperature sits at
                    <strong>{global_avg_temp:,.2f} °C</strong>, with a year-on-year change of
                    <strong>{yoy_temp_change:+.1f}%</strong> where prior data is available.
                    The hottest country in {latest_year} is <strong>{hottest_country}</strong>,
                    while composite climate risk is currently highest in
                    <strong>{risk_hotspot}</strong>.
                </p>
                <p style="font-size:0.85rem; color:#64748b; margin-top:0.4rem; line-height:1.7;">
                    Extreme events registered: <strong>{extreme_events:,}</strong> in {latest_year},
                    indicating an overall risk level of <strong>{risk_level}</strong>.
                </p>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("Adjust filters to generate an executive insight summary.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []


if __name__ == "__main__":
    main()
