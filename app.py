import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Climate Intelligence Dashboard", layout="wide")

# ---------------- LOAD ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("GlobalWeatherRepository_Cleaned.csv")
    df.columns = df.columns.str.lower()
    return df

df = load_data()

# ---------------- COLUMN DETECTION ----------------
temp_col = [c for c in df.columns if "temp" in c][0]
rain_col = [c for c in df.columns if "precip" in c or "rain" in c][0]
wind_col = [c for c in df.columns if "wind" in c][0]
country_col = "country"

# DATE
date_col = [c for c in df.columns if "date" in c]
if date_col:
    df["date"] = pd.to_datetime(df[date_col[0]])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

# ---------------- EVENTS ----------------
temp_thr = df[temp_col].quantile(0.90)
rain_thr = df[rain_col].quantile(0.90)
wind_thr = df[wind_col].quantile(0.90)

df["event_type"] = "Normal"
df.loc[df[temp_col] >= temp_thr, "event_type"] = "Heatwave"
df.loc[df[rain_col] >= rain_thr, "event_type"] = "Heavy Rain"
df.loc[df[wind_col] >= wind_thr, "event_type"] = "High Wind"

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌍 Smart Filters")

countries = st.sidebar.multiselect(
    "Country", df[country_col].unique(),
    default=df[country_col].unique()
)

years = st.sidebar.slider(
    "Year",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

event_choice = st.sidebar.selectbox(
    "Event Type", ["All", "Heatwave", "Heavy Rain", "High Wind"]
)

filtered = df[df[country_col].isin(countries)]
filtered = filtered[(filtered["year"] >= years[0]) & (filtered["year"] <= years[1])]

if event_choice != "All":
    filtered = filtered[filtered["event_type"] == event_choice]

# ---------------- NAV ----------------
page = st.sidebar.radio("Navigate", [
    "Overview", "Temperature", "Rain & Wind",
    "Extreme Events", "Comparison", "Risk",
    "Heatmap", "Seasonal", "Correlation"
])

# ---------------- KPI FUNCTION ----------------
def show_kpis(data):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡 Avg Temp", round(data[temp_col].mean(), 2))
    c2.metric("🌧 Total Rain", round(data[rain_col].sum(), 2))
    c3.metric("💨 Avg Wind", round(data[wind_col].mean(), 2))
    c4.metric("🚨 Events", len(data[data["event_type"] != "Normal"]))

# =================================================
# 1 OVERVIEW
# =================================================
if page == "Overview":

    st.title("🌍 Executive Climate Overview")
    show_kpis(filtered)

    st.markdown("---")

    # 🌍 WORLD MAP
    st.subheader("🌍 Global Temperature Distribution")

    map_data = filtered.groupby(country_col)[temp_col].mean().reset_index()

    fig_map = px.choropleth(
        map_data,
        locations=country_col,
        locationmode="country names",
        color=temp_col,
        color_continuous_scale="RdYlBu_r"
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🍩 Event Distribution")
        st.plotly_chart(px.pie(filtered, names="event_type", hole=0.5),
                        use_container_width=True)

    with col2:
        st.subheader("📈 Temperature Trend")
        trend = filtered.groupby("year")[temp_col].mean().reset_index()
        st.plotly_chart(px.line(trend, x="year", y=temp_col, markers=True),
                        use_container_width=True)

    st.markdown("---")

    st.subheader("🏆 Top 5 Hottest Countries")
    top5 = map_data.sort_values(temp_col, ascending=False).head(5)
    st.plotly_chart(px.bar(top5, x=country_col, y=temp_col,
                           color=temp_col, text=temp_col),
                    use_container_width=True)

# =================================================
# 2 TEMPERATURE
# =================================================
elif page == "Temperature":

    st.title("🌡 Temperature Intelligence")
    show_kpis(filtered)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(px.histogram(filtered, x=temp_col),
                        use_container_width=True)

    with col2:
        st.plotly_chart(px.box(filtered, y=temp_col),
                        use_container_width=True)

    yearly = filtered.groupby("year")[temp_col].mean().reset_index()
    st.plotly_chart(px.area(yearly, x="year", y=temp_col),
                    use_container_width=True)

# =================================================
# 3 RAIN & WIND
# =================================================
elif page == "Rain & Wind":

    st.title("🌧 Rain & Wind Intelligence")
    show_kpis(filtered)

    trend = filtered.groupby("year")[[rain_col, wind_col]].mean().reset_index()
    st.plotly_chart(px.line(trend, x="year", y=[rain_col, wind_col]),
                    use_container_width=True)

    bar = filtered.groupby(country_col)[[rain_col, wind_col]].mean().reset_index()
    st.plotly_chart(px.bar(bar, x=country_col, y=[rain_col, wind_col],
                           barmode="group"),
                    use_container_width=True)

    st.plotly_chart(px.pie(filtered, names="event_type"),
                    use_container_width=True)

# =================================================
# 4 EXTREME EVENTS
# =================================================
elif page == "Extreme Events":

    st.title("🚨 Extreme Events Monitor")
    show_kpis(filtered)

    selected = st.selectbox("Event Filter",
                            ["All"] + list(filtered["event_type"].unique()))

    data = filtered if selected == "All" else filtered[filtered["event_type"] == selected]

    st.plotly_chart(px.pie(data, names="event_type"), use_container_width=True)

    timeline = data.groupby("month").size().reset_index(name="count")
    st.plotly_chart(px.bar(timeline, x="month", y="count"),
                    use_container_width=True)

    stacked = data.groupby(["month", "event_type"]).size().reset_index(name="count")
    st.plotly_chart(px.bar(stacked, x="month", y="count",
                           color="event_type"),
                    use_container_width=True)

# =================================================
# 5 COMPARISON
# =================================================
elif page == "Comparison":

    st.title("🌍 Regional Comparison")

    c1 = st.selectbox("Country A", countries)
    c2 = st.selectbox("Country B", countries)

    d1 = filtered[filtered[country_col] == c1]
    d2 = filtered[filtered[country_col] == c2]

    fig = go.Figure()

    fig.add_trace(go.Bar(name=c1,
                         x=["Temp", "Rain", "Wind"],
                         y=[d1[temp_col].mean(), d1[rain_col].mean(), d1[wind_col].mean()]))

    fig.add_trace(go.Bar(name=c2,
                         x=["Temp", "Rain", "Wind"],
                         y=[d2[temp_col].mean(), d2[rain_col].mean(), d2[wind_col].mean()]))

    st.plotly_chart(fig)

# =================================================
# 6 RISK
# =================================================
elif page == "Risk":

    st.title("⚠ Climate Risk Intelligence")

    filtered = filtered.copy()
    filtered["risk"] = filtered[temp_col] + filtered[rain_col] + filtered[wind_col]

    risk = filtered.groupby(country_col)["risk"].mean().reset_index()

    st.plotly_chart(px.bar(risk.sort_values("risk", ascending=False).head(10),
                           x=country_col, y="risk"),
                    use_container_width=True)

# =================================================
# 7 HEATMAP
# =================================================
elif page == "Heatmap":

    st.title("🔥 Temperature Heatmap")

    heat = filtered.pivot_table(values=temp_col, index="month", columns="year")

    st.plotly_chart(px.imshow(heat, color_continuous_scale="RdYlBu_r"),
                    use_container_width=True)

# =================================================
# 8 SEASONAL
# =================================================
elif page == "Seasonal":

    st.title("📅 Seasonal Trends")

    st.plotly_chart(px.line(filtered.groupby("month")[temp_col].mean().reset_index(),
                            x="month", y=temp_col),
                    use_container_width=True)

# =================================================
# 9 CORRELATION (FIXED)
# =================================================
elif page == "Correlation":

    st.title("📊 Correlation Matrix")

    corr = filtered.select_dtypes(include="number").corr().round(2)

    fig = px.imshow(
        corr,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1
    )

    fig.update_traces(
        text=corr.values,
        texttemplate="%{text}"
    )

    st.plotly_chart(fig, use_container_width=True)