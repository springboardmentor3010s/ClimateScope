import numpy as np
import plotly.express as px
import streamlit as st

from app import load_data, load_css, global_filters, render_kpi, section_header, make_chart_layout


def main():
    load_css()
    df = load_data()
    df_filt, country_sel, year_range = global_filters(df)

    st.markdown(
        """
        <div class="page-title">💧 Precipitation & Wind Intelligence</div>
        <div class="page-subtitle">
            Analyse rainfall volumes, wind regimes, gust patterns, and hydro-wind variability.
        </div>
        <div class="accent-line"></div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- KPIs ----------
    total_rainfall = df_filt["precip_mm"].sum()
    heavy_rain_days = int((df_filt["precip_mm"] > 50).sum())
    avg_wind = df_filt["wind_kph"].mean()
    high_wind_events = int((df_filt["wind_kph"] > 40).sum())
    max_wind = df_filt["wind_kph"].max()

    rainfall_variability = (
        df_filt["precip_mm"].std() / df_filt["precip_mm"].mean() * 100
        if df_filt["precip_mm"].mean() > 0
        else np.nan
    )

    # Gust analysis
    has_gust = "gust_kph" in df_filt.columns
    avg_gust = df_filt["gust_kph"].mean() if has_gust else np.nan
    max_gust = df_filt["gust_kph"].max() if has_gust else np.nan

    section_header("📈", "Precipitation & Wind Metrics")

    with st.container():

        render_kpi(
            "Total Rainfall",
            f"{total_rainfall:,.0f} mm" if not np.isnan(total_rainfall) else "–",
            meta=f"Period {year_range[0]}–{year_range[1]}",
        )
        render_kpi(
            "Heavy Rain Days",
            f"{heavy_rain_days:,}",
            meta="Precip > 50 mm",
            meta_is_positive=heavy_rain_days < 50,
        )
        render_kpi(
            "Average Wind Speed",
            f"{avg_wind:,.1f} kph" if not np.isnan(avg_wind) else "–",
            meta=f"Max: {max_wind:.1f} kph" if not np.isnan(max_wind) else None,
        )
        render_kpi(
            "High Wind Events",
            f"{high_wind_events:,}",
            meta="Wind > 40 kph",
            meta_is_positive=high_wind_events < 50,
        )
        render_kpi(
            "Rainfall Variability",
            f"{rainfall_variability:,.1f}%" if not np.isnan(rainfall_variability) else "–",
            meta="Coefficient of variation",
        )
        if has_gust:
            render_kpi(
                "Avg Gust Speed",
                f"{avg_gust:,.1f} kph" if not np.isnan(avg_gust) else "–",
                meta=f"Max: {max_gust:.1f} kph" if not np.isnan(max_gust) else None,
            )

        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Trends ----------
    section_header("📈", "Rainfall & Wind Trends")

    top_left, top_right = [st.container() for _ in range(2)]

    with top_left:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Temporal</div>'
            '<div class="panel-title">Rainfall Trend</div>',
            unsafe_allow_html=True,
        )
        if not df_filt.empty:
            rain_ts = df_filt.groupby("date")["precip_mm"].sum().reset_index()
            fig_rain = px.area(
                rain_ts, x="date", y="precip_mm",
                color_discrete_sequence=["#3b82f6"],
            )
            make_chart_layout(fig_rain, height=450)
            fig_rain.update_traces(
                line=dict(width=2, color="#3b82f6"),
                fillcolor="rgba(59,130,246,0.08)",
                hovertemplate="%{x|%b %Y}<br>Total: %{y:.0f} mm<extra></extra>",
            )
            fig_rain.update_layout(xaxis_title="Date", yaxis_title="Total Rainfall (mm)")
            st.plotly_chart(fig_rain, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No rainfall data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with top_right:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Temporal</div>'
            '<div class="panel-title">Wind Speed Trend</div>',
            unsafe_allow_html=True,
        )
        if not df_filt.empty:
            wind_ts = df_filt.groupby("date")["wind_kph"].mean().reset_index()
            fig_wind = px.area(
                wind_ts, x="date", y="wind_kph",
                color_discrete_sequence=["#8b5cf6"],
            )
            make_chart_layout(fig_wind, height=450)
            fig_wind.update_traces(
                line=dict(width=2, color="#8b5cf6"),
                fillcolor="rgba(139,92,246,0.08)",
                hovertemplate="%{x|%b %Y}<br>Avg Wind: %{y:.1f} kph<extra></extra>",
            )
            fig_wind.update_layout(xaxis_title="Date", yaxis_title="Avg Wind (kph)")
            st.plotly_chart(fig_wind, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No wind data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Scatter & Ranking ----------
    section_header("🔗", "Coupled Dynamics & Rankings")

    bottom_left, bottom_right = [st.container() for _ in range(2)]

    with bottom_left:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Coupled Dynamics</div>'
            '<div class="panel-title">Rainfall vs Wind Scatter</div>',
            unsafe_allow_html=True,
        )
        if not df_filt.empty:
            scatter_df = df_filt.sample(min(2000, len(df_filt)), random_state=42)
            fig_scatter = px.scatter(
                scatter_df, x="precip_mm", y="wind_kph",
                color="country", hover_data=["year", "month"],
                opacity=0.6,
            )
            make_chart_layout(fig_scatter, height=450)
            fig_scatter.update_layout(
                xaxis_title="Precipitation (mm)",
                yaxis_title="Wind Speed (kph)",
                showlegend=False,
            )
            st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No scatter data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with bottom_right:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Ranking</div>'
            '<div class="panel-title">Country Rainfall & Wind Ranking</div>',
            unsafe_allow_html=True,
        )
        if not df_filt.empty:
            rank_df = (
                df_filt.groupby("country")[["precip_mm", "wind_kph"]]
                .agg({"precip_mm": "sum", "wind_kph": "mean"})
                .reset_index()
                .rename(columns={"precip_mm": "total_rainfall", "wind_kph": "avg_wind"})
                .sort_values("total_rainfall", ascending=False)
                .head(15)
            )
            fig_rank = px.bar(
                rank_df, x="total_rainfall", y="country", orientation="h",
                color="avg_wind",
                color_continuous_scale=["#dbeafe", "#6366f1", "#4c1d95"],
            )
            make_chart_layout(fig_rank, height=500)
            fig_rank.update_layout(
                xaxis_title="Total Rainfall (mm)",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),
                coloraxis_colorbar=dict(title="Avg Wind<br>(kph)"),
            )
            st.plotly_chart(fig_rank, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No ranking data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Gust Analysis ----------
    if has_gust:
        section_header("🌪", "Gust Analysis")

        gust_col1, gust_col2 = [st.container() for _ in range(2)]

        with gust_col1:
            st.markdown(
                '<div class="glass-panel"><div class="panel-header">Distribution</div>'
                '<div class="panel-title">Wind Gust Distribution</div>',
                unsafe_allow_html=True,
            )
            fig_gd = px.histogram(
                df_filt, x="gust_kph", nbins=40,
                color_discrete_sequence=["#06b6d4"],
            )
            make_chart_layout(fig_gd, height=450)
            fig_gd.update_layout(xaxis_title="Gust Speed (kph)", yaxis_title="Count")
            st.plotly_chart(fig_gd, use_container_width=True, config={"displayModeBar": False})
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

        with gust_col2:
            st.markdown(
                '<div class="glass-panel"><div class="panel-header">Comparison</div>'
                '<div class="panel-title">Top 10 Gustiest Countries</div>',
                unsafe_allow_html=True,
            )
            gust_rank = (
                df_filt.groupby("country")["gust_kph"].mean().reset_index()
                .sort_values("gust_kph", ascending=False).head(10)
            )
            fig_gr = px.bar(
                gust_rank, x="gust_kph", y="country", orientation="h",
                text_auto=".1f",
                color="gust_kph",
                color_continuous_scale=["#cffafe", "#06b6d4", "#0e7490"],
            )
            make_chart_layout(fig_gr, height=450)
            fig_gr.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Avg Gust (kph)", yaxis_title="",
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig_gr, use_container_width=True, config={"displayModeBar": False})
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []


if __name__ == "__main__":
    main()
