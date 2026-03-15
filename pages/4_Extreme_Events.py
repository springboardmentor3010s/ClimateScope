# import streamlit as st
# import plotly.express as px
# from utils.load_data import load_data

# st.title("🚨 Extreme Weather Events")

# df = load_data()

# extreme = df[
#     (df["temperature_celsius"] > 40) |
#     (df["precip_mm"] > 100) |
#     (df["wind_kph"] > 60)
# ]

# st.metric("Total Extreme Events Detected", len(extreme))

# # Scatter Plot
# fig_scatter = px.scatter(
#     extreme,
#     x="temperature_celsius",
#     y="precip_mm",
#     color="country",
#     size="wind_kph",
#     title="Extreme Weather Events Distribution"
# )

# st.plotly_chart(fig_scatter)

# # Bar Chart
# st.subheader("Extreme Events by Country")

# event_count = extreme.groupby("country").size().reset_index(name="events")

# fig_bar = px.bar(
#     event_count,
#     x="country",
#     y="events",
#     title="Extreme Weather Events Count"
# )

# st.plotly_chart(fig_bar)

# # Pie Chart
# fig_pie = px.pie(
#     event_count,
#     names="country",
#     values="events",
#     title="Extreme Events Share"
# )

# st.plotly_chart(fig_pie)




import streamlit as st
import plotly.express as px
from utils.load_data import load_data

st.title("🚨 Extreme Weather Events Analysis")

# Load dataset
df = load_data()

# Detect extreme events
extreme = df[
    (df["temperature_celsius"] > 40) |
    (df["precip_mm"] > 50) |
    (df["wind_kph"] > 60)
]

# KPI metric
st.metric("Total Extreme Events Detected", len(extreme))


# ---------------- BAR CHART ----------------
st.subheader("Top Countries with Extreme Events")

event_counts = extreme.groupby("country").size().reset_index(name="events")

fig_bar = px.bar(
    event_counts.sort_values("events", ascending=False).head(15),
    x="country",
    y="events",
    color="events",
    title="Extreme Events by Country",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_bar, use_container_width=True)


# ---------------- PIE CHART ----------------
st.subheader("Extreme Event Type Distribution")

df["event_type"] = "Normal"

df.loc[df["temperature_celsius"] > 40, "event_type"] = "Heatwave"
df.loc[df["precip_mm"] > 50, "event_type"] = "Heavy Rain"
df.loc[df["wind_kph"] > 60, "event_type"] = "Storm"

event_type_counts = df["event_type"].value_counts().reset_index()
event_type_counts.columns = ["event_type", "count"]

fig_pie = px.pie(
    event_type_counts,
    names="event_type",
    values="count",
    title="Extreme Weather Event Types"
)

st.plotly_chart(fig_pie)


# ---------------- SCATTER CHART ----------------
st.subheader("Temperature vs Wind Speed")

fig_scatter = px.scatter(
    df,
    x="temperature_celsius",
    y="wind_kph",
    color="precip_mm",
    size="precip_mm",
    title="Weather Interaction"
)

st.plotly_chart(fig_scatter, use_container_width=True)


# ---------------- MONTHLY TREND ----------------
st.subheader("Monthly Extreme Weather Trend")

monthly_events = extreme.groupby("month").size().reset_index(name="events")

fig_line = px.line(
    monthly_events,
    x="month",
    y="events",
    markers=True,
    title="Extreme Weather Events by Month"
)

st.plotly_chart(fig_line)