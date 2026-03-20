# import streamlit as st
# import plotly.express as px
# from utils.load_data import load_data

# st.title("🌧 Precipitation & Wind Analysis")

# df = load_data()

# st.markdown("Analyze rainfall and wind speed patterns across countries.")

# # Scatter Plot
# st.subheader("Rainfall vs Wind Speed")

# fig_scatter = px.scatter(
#     df,
#     x="precip_mm",
#     y="wind_kph",
#     color="country",
#     size="humidity",
#     title="Rainfall vs Wind Speed Relationship"
# )

# st.plotly_chart(fig_scatter, use_container_width=True)

# # Bubble Chart
# st.subheader("Bubble Chart: Weather Interaction")

# fig_bubble = px.scatter(
#     df,
#     x="temperature_celsius",
#     y="wind_kph",
#     size="precip_mm",
#     color="country",
#     title="Temperature vs Wind Speed with Rainfall"
# )

# st.plotly_chart(fig_bubble, use_container_width=True)

# # Pie Chart
# st.subheader("Rainfall Contribution by Country")

# rain_data = df.groupby("country")["precip_mm"].sum().reset_index()

# fig_pie = px.pie(
#     rain_data,
#     names="country",
#     values="precip_mm",
#     title="Total Rainfall Distribution"
# )

# st.plotly_chart(fig_pie)

# # Area Chart
# st.subheader("Monthly Rainfall Trend")

# fig_area = px.area(
#     df,
#     x="month",
#     y="precip_mm",
#     color="country",
#     title="Monthly Rainfall Trend"
# )

# st.plotly_chart(fig_area)





# import streamlit as st
# import plotly.express as px
# import seaborn as sns
# import matplotlib.pyplot as plt
# from utils.load_data import load_data

# px.defaults.template = "plotly_dark"

# st.title("🌧 Rain & Wind")

# df = load_data()

# # ---------------- HEATMAP ----------------
# corr = df[["temperature_celsius","precip_mm","wind_kph","humidity"]].corr()

# fig, ax = plt.subplots()
# sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
# st.pyplot(fig)

# # ---------------- WIND ----------------
# fig = px.histogram(df, x="wind_kph", color="country")
# st.plotly_chart(fig)

# # ---------------- DENSITY ----------------
# fig = px.density_contour(df, x="temperature_celsius", y="precip_mm", color="country")
# st.plotly_chart(fig)

# # ---------------- BUBBLE ----------------
# fig = px.scatter(df, x="temperature_celsius", y="wind_kph",
#                  size="precip_mm", color="humidity")
# st.plotly_chart(fig)





import streamlit as st
import plotly.express as px
from utils.load_data import load_data

px.defaults.template = "plotly_dark"

st.title("🚨 Extreme Weather Events Analysis")

df = load_data()

# ---------------- SEARCH + ALL ----------------
st.subheader("🔎 Search / Select Country")

all_countries = sorted(df["country"].unique())

selected = st.selectbox(
    "Select Country",
    ["All"] + all_countries
)

if selected != "All":
    df = df[df["country"] == selected]

search_text = st.text_input("Type to search (optional)")

if search_text:
    df = df[df["country"].str.contains(search_text, case=False)]

# ---------------- VALIDATION ----------------
if len(df) == 0:
    st.warning("No data available for selected filters")
    st.stop()

# ---------------- EXTREME EVENTS ----------------
extreme = df[
    (df["temperature_celsius"] > 40) |
    (df["precip_mm"] > 50) |
    (df["wind_kph"] > 60)
]

# KPI
st.metric("⚠ Total Extreme Events", len(extreme))

# ---------------- BAR ----------------
st.subheader("📊 Extreme Events by Country")

event_counts = extreme.groupby("country").size().reset_index(name="events")

fig_bar = px.bar(
    event_counts.sort_values("events", ascending=False),
    x="country",
    y="events",
    color="events",
    title="Extreme Events Count"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ---------------- HEATMAP ----------------
st.subheader("🔥 Extreme Event Heatmap")

heat = extreme.groupby(["month","country"]).size().reset_index(name="events")

fig_heat = px.density_heatmap(
    heat,
    x="month",
    y="country",
    z="events",
    title="Event Frequency Heatmap"
)

st.plotly_chart(fig_heat, use_container_width=True)

# ---------------- SCATTER ----------------
st.subheader("⚡ Event Severity Analysis")

fig_scatter = px.scatter(
    extreme,
    x="temperature_celsius",
    y="precip_mm",
    size="wind_kph",
    color="country",
    title="Extreme Event Distribution"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------- MONTHLY TREND ----------------
st.subheader("📈 Monthly Extreme Event Trend")

monthly = extreme.groupby("month").size().reset_index(name="events")

fig_line = px.line(
    monthly,
    x="month",
    y="events",
    markers=True,
    title="Extreme Events Trend"
)

st.plotly_chart(fig_line, use_container_width=True)