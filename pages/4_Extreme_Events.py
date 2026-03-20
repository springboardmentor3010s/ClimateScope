


# import streamlit as st
# import plotly.express as px
# from utils.load_data import load_data

# px.defaults.template = "plotly_dark"

# st.title("🚨 Extreme Events")

# df = load_data()

# extreme = df[(df["temperature_celsius"]>40) |
#              (df["precip_mm"]>50) |
#              (df["wind_kph"]>60)]

# st.metric("Events", len(extreme))

# # ---------------- BAR ----------------
# fig = px.bar(extreme.groupby("country").size().reset_index(name="events"),
#              x="country", y="events", color="events")
# st.plotly_chart(fig)

# # ---------------- HEATMAP ----------------
# heat = extreme.groupby(["month","country"]).size().reset_index(name="events")

# fig = px.density_heatmap(heat, x="month", y="country", z="events")
# st.plotly_chart(fig)

# # ---------------- SCATTER ----------------
# fig = px.scatter(extreme, x="temperature_celsius", y="precip_mm",
#                  size="wind_kph", color="country")
# st.plotly_chart(fig)





import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from utils.load_data import load_data

px.defaults.template = "plotly_dark"

st.title("🌧 Precipitation & Wind Analysis")

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

# ---------------- CORRELATION HEATMAP ----------------
st.subheader("🔥 Weather Correlation Heatmap")

corr = df[["temperature_celsius","precip_mm","wind_kph","humidity"]].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# ---------------- WIND HISTOGRAM ----------------
st.subheader("🌪 Wind Speed Distribution")

fig_wind = px.histogram(
    df,
    x="wind_kph",
    color="country",
    nbins=20,
    title="Wind Speed Distribution"
)

st.plotly_chart(fig_wind, use_container_width=True)

# ---------------- RAINFALL DENSITY ----------------
st.subheader("🌧 Rainfall Density Analysis")

fig_density = px.density_contour(
    df,
    x="temperature_celsius",
    y="precip_mm",
    color="country",
    title="Rainfall vs Temperature Density"
)

st.plotly_chart(fig_density, use_container_width=True)

# ---------------- BUBBLE CHART ----------------
st.subheader("🫧 Weather Interaction")

fig_bubble = px.scatter(
    df,
    x="temperature_celsius",
    y="wind_kph",
    size="precip_mm",
    color="humidity",
    title="Temperature vs Wind vs Rainfall"
)

st.plotly_chart(fig_bubble, use_container_width=True)

# ---------------- MONTHLY RAIN ----------------
st.subheader("📊 Monthly Rainfall Trend")

monthly = df.groupby("month")["precip_mm"].mean().reset_index()

fig_month = px.bar(
    monthly,
    x="month",
    y="precip_mm",
    color="precip_mm",
    title="Average Monthly Rainfall"
)

st.plotly_chart(fig_month, use_container_width=True)