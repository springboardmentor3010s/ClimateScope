# import streamlit as st
# import plotly.express as px
# from utils.load_data import load_data

# st.title("⚠ Climate Risk Intelligence")

# df = load_data()

# # Risk score calculation
# df["risk_score"] = (
#     df["temperature_celsius"]*0.4 +
#     df["precip_mm"]*0.3 +
#     df["wind_kph"]*0.3
# )

# risk = df.groupby("country")["risk_score"].mean().reset_index()

# # Bar Chart
# fig_bar = px.bar(
#     risk.sort_values("risk_score",ascending=False),
#     x="country",
#     y="risk_score",
#     color="risk_score",
#     title="Climate Risk Score by Country"
# )

# st.plotly_chart(fig_bar)

# # Pie Chart
# fig_pie = px.pie(
#     risk,
#     names="country",
#     values="risk_score",
#     title="Risk Distribution"
# )

# st.plotly_chart(fig_pie)

# # Scatter Chart
# fig_scatter = px.scatter(
#     df,
#     x="temperature_celsius",
#     y="precip_mm",
#     color="risk_score",
#     size="wind_kph",
#     title="Climate Risk Pattern"
# )

# st.plotly_chart(fig_scatter)





# import streamlit as st
# import plotly.express as px
# from utils.load_data import load_data

# st.title("⚠ Climate Risk Intelligence")

# df = load_data()

# # ---------------- NORMALIZATION ----------------
# df["temp_n"] = df["temperature_celsius"]/df["temperature_celsius"].max()
# df["rain_n"] = df["precip_mm"]/df["precip_mm"].max()
# df["wind_n"] = df["wind_kph"]/df["wind_kph"].max()

# df["risk_score"] = (
#     df["temp_n"]*0.5 +
#     df["rain_n"]*0.3 +
#     df["wind_n"]*0.2
# )

# # ---------------- HEALTH ----------------
# df["health"] = 100 - (df["risk_score"]*100)

# st.metric("🌱 Climate Health", f"{df['health'].mean():.2f}")

# # ---------------- BAR ----------------
# fig = px.bar(
#     df.groupby("country")["risk_score"].mean().reset_index(),
#     x="country",
#     y="risk_score",
#     color="risk_score"
# )

# st.plotly_chart(fig)





# import streamlit as st
# import plotly.express as px
# from utils.load_data import load_data

# px.defaults.template = "plotly_dark"

# st.title("⚠ Risk Intelligence")

# df = load_data()

# # ---------------- RISK ----------------
# df["temp_n"] = df["temperature_celsius"]/df["temperature_celsius"].max()
# df["rain_n"] = df["precip_mm"]/df["precip_mm"].max()
# df["wind_n"] = df["wind_kph"]/df["wind_kph"].max()

# df["risk"] = df["temp_n"]*0.5 + df["rain_n"]*0.3 + df["wind_n"]*0.2
# df["health"] = 100 - (df["risk"]*100)

# st.metric("Health Score", f"{df['health'].mean():.2f}")

# # ---------------- BAR ----------------
# fig = px.bar(df.groupby("country")["risk"].mean().reset_index(),
#              x="country", y="risk", color="risk")
# st.plotly_chart(fig)

# # ---------------- SCATTER ----------------
# fig = px.scatter(df, x="risk", y="health",
#                  color="country", size="wind_kph")
# st.plotly_chart(fig)

# # ---------------- HIST ----------------
# fig = px.histogram(df, x="risk", color="country")
# st.plotly_chart(fig)



import streamlit as st
import plotly.express as px
from utils.load_data import load_data

px.defaults.template = "plotly_dark"

st.title("⚠ Climate Risk Intelligence")

df = load_data()

# ---------------- SEARCH + ALL ----------------
st.subheader("🔎 Search Country")

all_countries = sorted(df["country"].unique())

selected = st.selectbox(
    "Search or Select Country",
    ["All"] + all_countries
)

# Apply filter
if selected != "All":
    df = df[df["country"] == selected]

# ---------------- OPTIONAL TEXT SEARCH ----------------
search_text = st.text_input("Type to search (optional)")

if search_text:
    df = df[df["country"].str.contains(search_text, case=False)]

# ---------------- RISK CALCULATION ----------------
df = df.copy()

df["temp_n"] = df["temperature_celsius"] / df["temperature_celsius"].max()
df["rain_n"] = df["precip_mm"] / df["precip_mm"].max()
df["wind_n"] = df["wind_kph"] / df["wind_kph"].max()

df["risk_score"] = (
    df["temp_n"] * 0.5 +
    df["rain_n"] * 0.3 +
    df["wind_n"] * 0.2
)

df["health_score"] = 100 - (df["risk_score"] * 100)

# ---------------- KPI ----------------
st.subheader("🌱 Climate Health Overview")

st.metric("Average Climate Health", f"{df['health_score'].mean():.2f}")

# ---------------- BAR ----------------
st.subheader("📊 Risk Score by Country")

risk_df = df.groupby("country")["risk_score"].mean().reset_index()

fig_bar = px.bar(
    risk_df.sort_values("risk_score", ascending=False),
    x="country",
    y="risk_score",
    color="risk_score",
    title="Climate Risk Score by Country"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ---------------- SCATTER ----------------
st.subheader("🎯 Risk vs Health Analysis")

fig_scatter = px.scatter(
    df,
    x="risk_score",
    y="health_score",
    color="country",
    size="wind_kph",
    title="Risk vs Health Relationship"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------- HIST ----------------
st.subheader("📊 Risk Distribution")

fig_hist = px.histogram(
    df,
    x="risk_score",
    nbins=30,
    color="country",
    title="Risk Score Distribution"
)

st.plotly_chart(fig_hist, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.subheader("📋 Filtered Data Preview")

st.dataframe(df.head(50), use_container_width=True)