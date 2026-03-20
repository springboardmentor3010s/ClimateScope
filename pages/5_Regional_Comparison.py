



# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
# from utils.load_data import load_data

# px.defaults.template = "plotly_dark"

# st.title("🌍 Regional Comparison")

# df = load_data()

# categories = ["temperature_celsius","precip_mm","wind_kph","humidity"]
# avg = df.groupby("country")[categories].mean().reset_index()

# # ---------------- RADAR ----------------
# fig = go.Figure()

# for i in range(len(avg)):
#     fig.add_trace(go.Scatterpolar(
#         r=avg.loc[i,categories],
#         theta=categories,
#         fill='toself',
#         name=avg.loc[i,"country"]
#     ))

# st.plotly_chart(fig)

# # ---------------- PARALLEL ----------------
# fig = px.parallel_coordinates(
#     df,
#     color="temperature_celsius",
#     dimensions=categories
# )

# st.plotly_chart(fig)

# # ---------------- RANK ----------------
# rank = df.groupby("country")["temperature_celsius"].mean().reset_index()

# fig = px.bar(rank.sort_values("temperature_celsius", ascending=False),
#              x="country", y="temperature_celsius")

# st.plotly_chart(fig)



import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.load_data import load_data

px.defaults.template = "plotly_dark"

st.title("🌍 Regional Climate Comparison")

df = load_data()

# ---------------- SEARCH + ALL ----------------
st.subheader("🔎 Search / Select Country")

all_countries = sorted(df["country"].unique())

selected = st.selectbox(
    "Select Country",
    ["All"] + all_countries
)

# Apply dropdown filter
if selected != "All":
    df = df[df["country"] == selected]

# Text search
search_text = st.text_input("Type to search (optional)")

if search_text:
    df = df[df["country"].str.contains(search_text, case=False)]

# ---------------- VALIDATION ----------------
if len(df) == 0:
    st.warning("No data available for selected filters")
    st.stop()

# ---------------- RADAR CHART ----------------
st.subheader("🕸 Climate Indicator Radar")

categories = ["temperature_celsius","precip_mm","wind_kph","humidity"]

avg = df.groupby("country")[categories].mean().reset_index()

fig_radar = go.Figure()

for i in range(len(avg)):
    fig_radar.add_trace(go.Scatterpolar(
        r=avg.loc[i, categories],
        theta=categories,
        fill='toself',
        name=avg.loc[i, "country"]
    ))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True
)

st.plotly_chart(fig_radar, use_container_width=True)

# ---------------- PARALLEL COORDINATES ----------------
st.subheader("📊 Multi-Dimensional Comparison")

fig_parallel = px.parallel_coordinates(
    df,
    color="temperature_celsius",
    dimensions=categories,
    title="Climate Parameter Comparison"
)

st.plotly_chart(fig_parallel, use_container_width=True)

# ---------------- COUNTRY RANKING ----------------
st.subheader("🏆 Temperature Ranking")

rank_df = df.groupby("country")["temperature_celsius"].mean().reset_index()

fig_rank = px.bar(
    rank_df.sort_values("temperature_celsius", ascending=False),
    x="country",
    y="temperature_celsius",
    color="temperature_celsius",
    title="Country Ranking by Temperature"
)

st.plotly_chart(fig_rank, use_container_width=True)

# ---------------- TREND ----------------
st.subheader("📈 Temperature Trend")

trend_df = df.groupby(["year","country"])["temperature_celsius"].mean().reset_index()

fig_trend = px.line(
    trend_df,
    x="year",
    y="temperature_celsius",
    color="country",
    markers=True,
    title="Temperature Trend Comparison"
)

st.plotly_chart(fig_trend, use_container_width=True)