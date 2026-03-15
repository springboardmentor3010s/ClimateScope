# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Load data
# df = pd.read_csv("data/cleaned_weather_monthly.csv")

# st.set_page_config(layout="wide")
# st.title("🌍 ClimateScope - Global Climate Dashboard")

# # Sidebar Filters
# st.sidebar.header("Filters")

# selected_country = st.sidebar.selectbox(
#     "Select Country",
#     df['country'].unique()
# )

# selected_year = st.sidebar.selectbox(
#     "Select Year",
#     sorted(df['year'].unique())
# )

# selected_metric = st.sidebar.selectbox(
#     "Select Metric",
#     ["temperature_celsius", "precip_mm", "wind_kph", "humidity"]
# )

# filtered_df = df[
#     (df['country'] == selected_country) &
#     (df['year'] == selected_year)
# ]

# # 🌍 Global Map
# st.subheader("Global Temperature Distribution")

# fig_map = px.choropleth(
#     df[df['year'] == selected_year],
#     locations="country",
#     locationmode="country names",
#     color=selected_metric,
#     title="Global Distribution"
# )

# st.plotly_chart(fig_map, use_container_width=True)

# # 📈 Monthly Trend
# st.subheader("Monthly Trend")

# fig_line = px.line(
#     filtered_df,
#     x="month",
#     y=selected_metric,
#     title=f"{selected_metric} Trend - {selected_country}"
# )

# st.plotly_chart(fig_line, use_container_width=True)

# # 📊 Correlation Heatmap
# st.subheader("Correlation Heatmap")

# corr = df[['temperature_celsius','humidity','wind_kph','precip_mm','pressure_mb']].corr()

# fig, ax = plt.subplots()
# sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
# st.pyplot(fig)












import streamlit as st #Ml3
from utils.load_data import load_data

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

st.markdown("""
This dashboard provides insights into global climate trends including:

- Temperature intelligence
- Rainfall and wind analysis
- Extreme climate events
- Regional comparison
- Climate risk indicators
""")

# df = load_data()

# st.subheader("Dataset Preview")

# st.dataframe(df.head())


# st.sidebar.header("🌐 Global Filters")

# country = st.sidebar.selectbox(
#     "Select Country",
#     df["country"].unique()
# )

# year = st.sidebar.selectbox(
#     "Select Year",
#     sorted(df["year"].unique())
# )

# metric = st.sidebar.selectbox(
#     "Select Metric",
#     ["temperature_celsius","precip_mm","wind_kph","humidity"]
# )

# filtered_df = df[(df["country"] == country) & (df["year"] == year)]


df = load_data()

# Sidebar filters
selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["country"].unique())
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + sorted(df["year"].unique())
)


# metric = st.sidebar.selectbox(
#     "Select Metric",
#     ["temperature_celsius","precip_mm","wind_kph","humidity"]

# Apply filters


filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["year"] == selected_year]

# Show table
st.subheader("Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)






st.subheader("📊 Filtered Dataset Preview")

# Apply filters first
filtered_df = df.copy()

selected_country = st.session_state.get("country_filter", "All")
selected_year = st.session_state.get("year_filter", "All")

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["year"] == selected_year]

# Show number of rows
st.write(f"Total Records: {len(filtered_df)}")

# -----------------------
# SEARCH FUNCTION
# -----------------------

search = st.text_input("🔎 Search Country")

if search:
    filtered_df = filtered_df[
        filtered_df["country"].str.contains(search, case=False)
    ]

# -----------------------
# PAGINATION
# -----------------------

rows_per_page = 10
page = st.number_input("Page", min_value=1, step=1)

start = (page - 1) * rows_per_page
end = start + rows_per_page

paginated_df = filtered_df.iloc[start:end]

st.dataframe(
    paginated_df,
    use_container_width=True
)

# -----------------------
# DOWNLOAD BUTTON
# -----------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_climate_data.csv",
    mime="text/csv"
)