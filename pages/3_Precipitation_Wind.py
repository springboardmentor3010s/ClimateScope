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






import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from utils.load_data import load_data

st.title("🌧 Precipitation & Wind Analysis")

df = load_data()

st.markdown("Analyze rainfall and wind speed patterns across countries.")

# ---------------- CORRELATION HEATMAP ----------------
st.subheader("Weather Correlation Heatmap")

corr = df[["temperature_celsius","precip_mm","wind_kph","humidity","pressure_mb"]].corr()

fig, ax = plt.subplots()

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)


# ---------------- BUBBLE CHART ----------------
st.subheader("Weather Interaction Bubble Chart")

fig_bubble = px.scatter(
    df,
    x="temperature_celsius",
    y="wind_kph",
    size="precip_mm",
    color="humidity",
    title="Temperature vs Wind Speed with Rainfall",
    color_continuous_scale="viridis"
)

st.plotly_chart(fig_bubble, use_container_width=True)


# ---------------- PIE CHART ----------------
# st.subheader("Rainfall Contribution by Country")

# rain_data = df.groupby("country")["precip_mm"].sum().reset_index()

# fig_pie = px.pie(
#     rain_data.sort_values("precip_mm", ascending=False).head(10),
#     names="country",
#     values="precip_mm",
#     title="Top 10 Countries by Rainfall"
# )

# st.plotly_chart(fig_pie)


# Pie Chart
st.subheader("Rainfall Contribution by Country")
rain_data = df.groupby("country")["precip_mm"].sum().reset_index()
fig_pie = px.pie(
    rain_data.sort_values("precip_mm", ascending=False).head(35),
    names="country",
            values="precip_mm",
     title="Total Rainfall Distribution"
)
st.plotly_chart(fig_pie)


# ---------------- MONTHLY RAINFALL BAR CHART ----------------
st.subheader("Monthly Average Rainfall")

monthly_rain = df.groupby("month")["precip_mm"].mean().reset_index()

fig_bar = px.bar(
    monthly_rain,
    x="month",
    y="precip_mm",
    color="precip_mm",
    title="Average Monthly Rainfall",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_bar, use_container_width=True)