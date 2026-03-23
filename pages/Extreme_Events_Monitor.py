import numpy as np
import plotly.express as px
import streamlit as st

from app import load_data, load_css, global_filters, render_kpi, section_header, make_chart_layout, get_map_colors


def compute_risk_label(total_events: int) -> str:
    if total_events < 50:
        return "🟢 Low"
    if total_events < 200:
        return "🟡 Medium"
    return "🔴 High"


def risk_badge(label: str) -> str:
    if "Low" in label:
        return "stat-badge-green"
    if "Medium" in label:
        return "stat-badge-amber"
    return "stat-badge-red"


def main():
    load_css()
    df = load_data()
    df_filt, country_sel, year_range = global_filters(df)

    st.markdown(
        """
        <div class="page-title">🚨 Extreme Events Monitor</div>
        <div class="page-subtitle">
            Track heatwaves, heavy rain, and high-wind events against defined thresholds.
        </div>
        <div class="accent-line"></div>
        """,
        unsafe_allow_html=True,
    )

    # Thresholds: Temp > 40°C, Rain > 100 mm, Wind > 60 kph
    extreme = df_filt[
        (df_filt["temperature_celsius"] > 40)
        | (df_filt["precip_mm"] > 100)
        | (df_filt["wind_kph"] > 60)
    ].copy()

    total_extreme = int(extreme.shape[0])
    heatwave_days = int((df_filt["temperature_celsius"] > 40).sum())
    heavy_rain_events = int((df_filt["precip_mm"] > 100).sum())
    high_wind_events = int((df_filt["wind_kph"] > 60).sum())
    highest_risk_country = (
        extreme["country"].value_counts().idxmax() if not extreme.empty else "N/A"
    )

    risk_label = compute_risk_label(total_extreme)

    # ---------- KPIs ----------
    section_header("📈", "Extreme Event Metrics")

    with st.container():

        render_kpi(
            "Total Extreme Events", f"{total_extreme:,}",
            meta=f"{risk_label}",
            meta_is_positive=total_extreme < 50,
        )
        render_kpi(
            "Heatwave Days", f"{heatwave_days:,}",
            meta=f"Temp > 40°C",
            meta_is_positive=heatwave_days < 50,
        )
        render_kpi(
            "Heavy Rain Events", f"{heavy_rain_events:,}",
            meta=f"Precip > 100 mm",
            meta_is_positive=heavy_rain_events < 50,
        )
        render_kpi(
            "High Wind Events", f"{high_wind_events:,}",
            meta=f"Wind > 60 kph",
            meta_is_positive=high_wind_events < 50,
        )
        render_kpi(
            "Highest Risk Country", highest_risk_country,
            meta="Most extreme events",
            meta_is_positive=False,
        )

        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # Risk Badge
    badge_cls = risk_badge(risk_label)
    st.markdown(
        f"""
        <div style="display:flex; gap:0.5rem; margin-bottom:1rem; flex-wrap:wrap;">
            <span class="stat-badge {badge_cls}">Risk Level: {risk_label}</span>
            <span class="stat-badge stat-badge-amber">🔥 {heatwave_days} Heatwaves</span>
            <span class="stat-badge stat-badge-blue">🌧 {heavy_rain_events} Heavy Rain</span>
            <span class="stat-badge stat-badge-purple">💨 {high_wind_events} High Wind</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Timeline + Map ----------
    section_header("📈", "Timeline & Spatial Distribution")

    top_left, top_right = [st.container() for _ in range(2)]

    with top_left:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Temporal</div>'
            '<div class="panel-title">Extreme Event Timeline</div>',
            unsafe_allow_html=True,
        )
        if not extreme.empty:
            timeline = extreme.groupby("date")["has_extreme_event"].sum().reset_index()
            fig_tl = px.bar(
                timeline, x="date", y="has_extreme_event",
                color_discrete_sequence=["#ef4444"],
            )
            make_chart_layout(fig_tl, height=450)
            fig_tl.update_traces(
                hovertemplate="%{x|%b %Y}<br>Events: %{y}<extra></extra>",
                opacity=0.85,
            )
            fig_tl.update_layout(xaxis_title="Date", yaxis_title="Extreme Events")
            st.plotly_chart(fig_tl, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No extreme events in selected period.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    with top_right:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Spatial</div>'
            '<div class="panel-title">Country Extreme Event Map</div>',
            unsafe_allow_html=True,
        )
        if not extreme.empty:
            map_df = extreme.groupby("country")["has_extreme_event"].sum().reset_index()
            fig_map = px.choropleth(
                map_df, locations="country", locationmode="country names",
                color="has_extreme_event",
                color_continuous_scale=["#fef3c7", "#f97316", "#dc2626"],
            )
            make_chart_layout(fig_map, height=450)
            map_colors = get_map_colors()
            fig_map.update_layout(
                coloraxis_colorbar=dict(title="Events"),
                geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False,
                         showcoastlines=True, coastlinecolor=map_colors["coastlinecolor"],
                         landcolor=map_colors["landcolor"], lakecolor=map_colors["lakecolor"]),
            )
            fig_map.update_traces(
                hovertemplate="<b>%{location}</b><br>Events: %{z}<extra></extra>"
            )
            st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No spatial data.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Heatmap + Distribution ----------
    section_header("🔥", "Seasonality & Event Breakdown")

    bottom_left, bottom_right = [st.container() for _ in range(2)]

    with bottom_left:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Seasonality</div>'
            '<div class="panel-title">Monthly Extreme Event Heatmap</div>',
            unsafe_allow_html=True,
        )
        if not extreme.empty:
            hm = extreme.groupby(["year", "month"])["has_extreme_event"].sum().reset_index()
            month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                           7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
            hm_pivot = hm.pivot(index="year", columns="month", values="has_extreme_event")
            hm_pivot = hm_pivot.rename(columns=month_names)
            fig_hm = px.imshow(
                hm_pivot,
                color_continuous_scale=["#fff7ed", "#f97316", "#991b1b"],
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

    with bottom_right:
        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Breakdown</div>'
            '<div class="panel-title">Event Type Distribution</div>',
            unsafe_allow_html=True,
        )

        event_data = {
            "Event Type": ["🔥 Heatwave", "🌧 Heavy Rain", "💨 High Wind"],
            "Count": [heatwave_days, heavy_rain_events, high_wind_events],
        }
        import pandas as pd
        event_df = pd.DataFrame(event_data)

        if event_df["Count"].sum() > 0:
            pie_col, bar_col = [st.container() for _ in range(2)]

            with pie_col:
                fig_pie = px.pie(
                    event_df, names="Event Type", values="Count",
                    color_discrete_sequence=["#ef4444", "#3b82f6", "#8b5cf6"],
                    hole=0.45,
                )
                make_chart_layout(fig_pie, height=450)
                fig_pie.update_traces(textposition="inside", textinfo="percent+label")
                st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

            with bar_col:
                fig_bar = px.bar(
                    event_df, x="Event Type", y="Count",
                    color="Event Type",
                    color_discrete_sequence=["#ef4444", "#3b82f6", "#8b5cf6"],
                    text_auto=True,
                )
                make_chart_layout(fig_bar, height=450)
                fig_bar.update_layout(showlegend=False, xaxis_title="", yaxis_title="Count")
                st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No extreme events to show.")
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []

    # ---------- Country Distribution ----------
    if not extreme.empty:
        section_header("🌍", "Country-Level Analysis")

        st.markdown(
            '<div class="glass-panel"><div class="panel-header">Distribution</div>'
            '<div class="panel-title">Extreme Events by Country (Top 15)</div>',
            unsafe_allow_html=True,
        )
        dist_df = (
            extreme.groupby("country")["has_extreme_event"].sum().reset_index()
            .sort_values("has_extreme_event", ascending=False).head(15)
        )
        fig_dist = px.bar(
            dist_df, x="has_extreme_event", y="country", orientation="h",
            text_auto=True, color="has_extreme_event",
            color_continuous_scale=["#fde68a", "#f97316", "#dc2626"],
        )
        make_chart_layout(fig_dist, height=500)
        fig_dist.update_layout(
            coloraxis_showscale=False,
            xaxis_title="Extreme Events", yaxis_title="",
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})
        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []


if __name__ == "__main__":
    main()
