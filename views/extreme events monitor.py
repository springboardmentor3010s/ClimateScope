import streamlit as st
import numpy as np
import plotly.express as px

from utils import CLIMATE_CONTINUOUS, CLIMATE_PALETTE


def render(df, selected_country="All", selected_year="All"):
    st.title("🚨 Extreme Events Monitor")
    st.write("This dashboard detects climate anomalies such as heatwaves, heavy rainfall and strong winds.")

    filtered = df.copy()
    if selected_country != "All":
        filtered = filtered[filtered["country"] == selected_country]
    if selected_year != "All":
        filtered = filtered[filtered["year"] == selected_year]

    heatwave = filtered[filtered["temperature_celsius"] > 40]
    heavy_rain = filtered[filtered["precip_mm"] > 100]
    high_wind = filtered[filtered["wind_kph"] > 60]

    extreme = filtered[
        (filtered["temperature_celsius"] > 40)
        | (filtered["precip_mm"] > 100)
        | (filtered["wind_kph"] > 60)
    ]

    # KPIs
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Extreme Events", len(extreme))
    c2.metric("Heatwave Days", len(heatwave))
    c3.metric("Heavy Rain Events", len(heavy_rain))
    c4.metric("High Wind Events", len(high_wind))

    risk_country = "—"
    if not extreme.empty:
        risk_country = extreme.groupby("country").size().idxmax()

    c5.metric("Highest Risk Country", risk_country)

    events = len(extreme)
    if events < 50:
        risk = "🟢 Low"
    elif events < 150:
        risk = "🟡 Medium"
    else:
        risk = "🔴 High"

    st.metric("Global Risk Level", risk)

    # Timeline
    st.subheader("Extreme Event Timeline")
    timeline = extreme.groupby("year").size().reset_index(name="events")

    fig = px.line(timeline, x="year", y="events")
    st.plotly_chart(fig, width="stretch", key="eem_timeline")

    # Timeline Insight
    if len(timeline) > 1:
        pct_change = ((timeline["events"].iloc[-1] - timeline["events"].iloc[0]) / timeline["events"].iloc[0]) * 100 if timeline["events"].iloc[0] != 0 else 0
        change_direction = "increase" if pct_change > 0 else "decrease" if pct_change < 0 else "remain stable"
        st.info(f"Insight: Extreme events have {change_direction}d by {abs(pct_change):.1f}% from {int(timeline['year'].iloc[0])} to {int(timeline['year'].iloc[-1])}.")
    else:
        st.info("Insight: Not enough data to compute trend changes over time.")

    # Country Map
    st.subheader("Country-wise Extreme Event Map")
    country_events = extreme.groupby("country").size().reset_index(name="events")

    fig2 = px.choropleth(
        country_events,
        locations="country",
        locationmode="country names",
        color="events",
    )
    st.plotly_chart(fig2, width="stretch", key="eem_country_map")

    if not country_events.empty:
        top_country = country_events.loc[country_events["events"].idxmax()]
        st.info(f"Insight: {top_country['country']} leads with {top_country['events']} extreme events in the selected period.")
    else:
        st.info("Insight: No countries have recorded extreme events for the selected filters.")

    # Monthly Heatmap
    st.subheader("Monthly Extreme Event Heatmap")
    heat = extreme.pivot_table(index="year", columns="month", values="temperature_celsius", aggfunc="count")

    fig3 = px.imshow(heat, aspect="auto")
    st.plotly_chart(fig3, width="stretch", key="eem_monthly_heatmap")

    if not heat.empty and np.isfinite(np.nanmax(heat.values)):
        max_idx = np.nanargmax(heat.values)
        max_year, max_month = divmod(max_idx, heat.shape[1])
        max_value = np.nanmax(heat.values)
        month_label = heat.columns[max_month]
        year_label = heat.index[max_year]
        st.info(
            f"Insight: Peak extreme activity occurred in {month_label} {year_label} with {int(max_value)} events."
        )
    else:
        st.info("Insight: Not enough data to render a monthly heatmap.")

    # Event Distribution
    st.subheader("Event Distribution by Type")
    event_data = {
        "Event": ["Heatwave", "Heavy Rain", "High Wind"],
        "Count": [len(heatwave), len(heavy_rain), len(high_wind)],
    }

    fig4 = px.pie(event_data, names="Event", values="Count")
    st.plotly_chart(fig4, width="stretch", key="eem_event_dist")

    total_events = sum(event_data["Count"])
    if total_events > 0:
        top_event = max(zip(event_data["Event"], event_data["Count"]), key=lambda x: x[1])
        share = (top_event[1] / total_events) * 100
        st.info(f"Insight: {top_event[0]} accounts for {share:.1f}% of extreme events in the selected data.")
    else:
        st.info("Insight: There are no extreme events for the selected filters.")

    st.markdown(
        "<div style='text-align:center; margin-top:2rem; font-size:0.9rem; color:rgba(255,255,255,0.8);'>"
        "<a href='#top' style='color:#80d4ff; text-decoration:none;'>⬆ Back to top</a>"
        "</div>",
        unsafe_allow_html=True,
    )
