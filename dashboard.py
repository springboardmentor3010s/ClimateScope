# import streamlit as st
# import pandas as pd
# from utils.load_data import load_data

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="ClimateScope Intelligence Dashboard",
#     page_icon="🌍",
#     layout="wide"
# )

# st.title("🌍 ClimateScope Global Climate Intelligence")

# st.markdown("""
# Advanced analytics platform for monitoring **temperature, rainfall, wind trends,
# and climate risk patterns** across countries.
# """)

# # ---------------- LOAD DATA ----------------
# df = load_data()

# # ---------------- SIDEBAR FILTERS ----------------
# st.sidebar.header("🔍 Advanced Filters")

# selected_countries = st.sidebar.multiselect(
#     "Select Countries",
#     df["country"].unique(),
#     default=df["country"].unique()[:5]
# )

# year_range = st.sidebar.slider(
#     "Select Year Range",
#     int(df["year"].min()),
#     int(df["year"].max()),
#     (int(df["year"].min()), int(df["year"].max()))
# )

# # Apply filters
# filtered_df = df[
#     (df["country"].isin(selected_countries)) &
#     (df["year"].between(year_range[0], year_range[1]))
# ]

# # ---------------- KPI SECTION ----------------
# st.subheader("📊 Global KPIs")

# col1, col2, col3, col4 = st.columns(4)

# col1.metric("🌡 Avg Temp", f"{filtered_df['temperature_celsius'].mean():.2f} °C")
# col2.metric("🔥 Max Temp", f"{filtered_df['temperature_celsius'].max():.2f} °C")
# col3.metric("🌧 Total Rain", f"{filtered_df['precip_mm'].sum():.0f} mm")
# col4.metric("💨 Avg Wind", f"{filtered_df['wind_kph'].mean():.2f} kph")

# # ---------------- CLIMATE HEALTH ----------------
# filtered_df["temp_n"] = filtered_df["temperature_celsius"] / filtered_df["temperature_celsius"].max()
# filtered_df["rain_n"] = filtered_df["precip_mm"] / filtered_df["precip_mm"].max()
# filtered_df["wind_n"] = filtered_df["wind_kph"] / filtered_df["wind_kph"].max()

# filtered_df["risk_score"] = (
#     filtered_df["temp_n"] * 0.5 +
#     filtered_df["rain_n"] * 0.3 +
#     filtered_df["wind_n"] * 0.2
# )

# filtered_df["health_score"] = 100 - (filtered_df["risk_score"] * 100)

# st.metric("🌱 Climate Health Score", f"{filtered_df['health_score'].mean():.2f}")

# # ---------------- AI INSIGHTS ----------------
# st.subheader("🧠 AI Insights Engine")

# def generate_insights(df):
#     insights = []

#     if len(df) == 0:
#         return ["No data available"]

#     hottest = df.groupby("country")["temperature_celsius"].mean().idxmax()
#     coldest = df.groupby("country")["temperature_celsius"].mean().idxmin()
#     rainy = df.groupby("country")["precip_mm"].sum().idxmax()

#     insights.append(f"🔥 Hottest Country: {hottest}")
#     insights.append(f"❄️ Coldest Country: {coldest}")
#     insights.append(f"🌧 Highest Rainfall: {rainy}")

#     extreme = len(df[df["temperature_celsius"] > 40])
#     insights.append(f"⚠️ Heatwave Events: {extreme}")

#     return insights

# for insight in generate_insights(filtered_df):
#     st.success(insight)

# # ---------------- SEARCH ----------------
# st.subheader("🔎 Smart Data Explorer")

# search = st.text_input("Search Country")

# if search:
#     filtered_df = filtered_df[
#         filtered_df["country"].str.contains(search, case=False)
#     ]

# # ---------------- PAGINATION ----------------
# rows_per_page = 10
# page = st.number_input("Page", min_value=1, step=1)

# start = (page - 1) * rows_per_page
# end = start + rows_per_page

# paginated_df = filtered_df.iloc[start:end]

# st.write(f"Showing {start+1} to {min(end, len(filtered_df))} of {len(filtered_df)} records")

# st.dataframe(paginated_df, use_container_width=True)

# # ---------------- DOWNLOAD ----------------
# st.download_button(
#     label="⬇ Download Filtered Data",
#     data=filtered_df.to_csv(index=False),
#     file_name="climate_filtered_data.csv",
#     mime="text/csv"
# )
import streamlit as st
import pandas as pd
from utils.load_data import load_data

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ClimateScope Intelligence Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 ClimateScope Global Climate Intelligence")

st.markdown("""
Advanced analytics platform for monitoring **temperature, rainfall, wind trends,
and climate risk patterns** across countries.
""")

# ---------------- LOAD DATA ----------------
df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Advanced Filters")

# -------- COUNTRY FILTER WITH ALL --------
all_countries = sorted(df["country"].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    ["All"] + all_countries,
    default=["All"]
)

# Fix: prevent "All + others"
if "All" in selected_countries and len(selected_countries) > 1:
    selected_countries = ["All"]

# -------- YEAR FILTER --------
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

# ---------------- APPLY FILTERS ----------------
if "All" in selected_countries:
    filtered_df = df.copy()
else:
    filtered_df = df[df["country"].isin(selected_countries)]

filtered_df = filtered_df[
    filtered_df["year"].between(year_range[0], year_range[1])
]

# ---------------- KPI SECTION ----------------
st.subheader("📊 Global KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡 Avg Temp", f"{filtered_df['temperature_celsius'].mean():.2f} °C")
col2.metric("🔥 Max Temp", f"{filtered_df['temperature_celsius'].max():.2f} °C")
col3.metric("🌧 Total Rain", f"{filtered_df['precip_mm'].sum():.0f} mm")
col4.metric("💨 Avg Wind", f"{filtered_df['wind_kph'].mean():.2f} kph")

# ---------------- CLIMATE HEALTH ----------------
filtered_df = filtered_df.copy()

filtered_df["temp_n"] = filtered_df["temperature_celsius"] / filtered_df["temperature_celsius"].max()
filtered_df["rain_n"] = filtered_df["precip_mm"] / filtered_df["precip_mm"].max()
filtered_df["wind_n"] = filtered_df["wind_kph"] / filtered_df["wind_kph"].max()

filtered_df["risk_score"] = (
    filtered_df["temp_n"] * 0.5 +
    filtered_df["rain_n"] * 0.3 +
    filtered_df["wind_n"] * 0.2
)

filtered_df["health_score"] = 100 - (filtered_df["risk_score"] * 100)

st.metric("🌱 Climate Health Score", f"{filtered_df['health_score'].mean():.2f}")

# ---------------- AI INSIGHTS ----------------
# ---------------- AI INSIGHTS + VISUALS ----------------
import plotly.express as px

st.subheader("🧠 AI Insights Engine (Visual Intelligence)")

def generate_insights_with_graphs(data):

    if len(data) == 0:
        st.warning("No data available")
        return

    # -------- HOTTEST COUNTRY --------
    hottest_df = data.groupby("country")["temperature_celsius"].mean().reset_index()
    hottest_df = hottest_df.sort_values("temperature_celsius", ascending=False)

    hottest_country = hottest_df.iloc[0]["country"]

    st.success(f"🔥 Hottest Country: {hottest_country}")

    fig1 = px.bar(
        hottest_df.head(10),
        x="country",
        y="temperature_celsius",
        color="temperature_celsius",
        title="Top 10 Hottest Countries"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # -------- COLDEST COUNTRY --------
    coldest_country = hottest_df.iloc[-1]["country"]

    st.success(f"❄️ Coldest Country: {coldest_country}")

    fig2 = px.bar(
        hottest_df.tail(10),
        x="country",
        y="temperature_celsius",
        color="temperature_celsius",
        title="Coldest Countries"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # -------- RAINFALL ANALYSIS --------
    rain_df = data.groupby("country")["precip_mm"].sum().reset_index()
    rain_df = rain_df.sort_values("precip_mm", ascending=False)

    rainy_country = rain_df.iloc[0]["country"]

    st.success(f"🌧 Highest Rainfall: {rainy_country}")

    fig3 = px.pie(
        rain_df.head(10),
        names="country",
        values="precip_mm",
        title="Top Rainfall Contribution"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # -------- EXTREME EVENTS --------
    extreme = data[data["temperature_celsius"] > 40]

    st.success(f"⚠️ Heatwave Events: {len(extreme)}")

    if len(extreme) > 0:
        fig4 = px.scatter(
            extreme,
            x="temperature_celsius",
            y="wind_kph",
            size="precip_mm",
            color="country",
            title="Heatwave Event Distribution"
        )
        st.plotly_chart(fig4, use_container_width=True)

    # -------- TREND INSIGHT --------
    trend = data.groupby("year")["temperature_celsius"].mean().reset_index()

    st.success("📈 Temperature trend over years")

    fig5 = px.line(
        trend,
        x="year",
        y="temperature_celsius",
        markers=True,
        title="Temperature Trend"
    )
    st.plotly_chart(fig5, use_container_width=True)


# CALL FUNCTION
generate_insights_with_graphs(filtered_df)
# ---------------- SEARCH ----------------
st.subheader("🔎 Smart Data Explorer")

search = st.text_input("Search Country")

if search:
    filtered_df = filtered_df[
        filtered_df["country"].str.contains(search, case=False)
    ]

# ---------------- PAGINATION ----------------
rows_per_page = 10
page = st.number_input("Page", min_value=1, step=1)

start = (page - 1) * rows_per_page
end = start + rows_per_page

paginated_df = filtered_df.iloc[start:end]

st.write(f"Showing {start+1} to {min(end, len(filtered_df))} of {len(filtered_df)} records")

st.dataframe(paginated_df, use_container_width=True)

# ---------------- DOWNLOAD ----------------
st.download_button(
    label="⬇ Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="climate_filtered_data.csv",
    mime="text/csv"
)