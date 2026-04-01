import importlib.util
from pathlib import Path

import pandas as pd
import plotly.io as pio
import streamlit as st

st.set_page_config(page_title="Global Climate Intelligence Dashboard", layout="wide")

# --- Plotly default theme (climate palette) --------------------------------
import plotly.graph_objs as go

climate_template = go.layout.Template(
    layout={
        "paper_bgcolor": "rgba(10, 25, 40, 0.85)",
        "plot_bgcolor": "argba(8, 24, 40, 0.75)",
        "font": {"family": "Rubik, Inter, sans-serif", "color": "#f2f8ff"},
        "legend": {"bgcolor": "rgba(0,0,0,0.30)", "bordercolor": "rgba(255,255,255,0.18)"},
        "hoverlabel": {
            "font": {"family": "Rubik, Inter, sans-serif", "size": 15, "color": "#ffffff"},
            "bgcolor": "rgba(10, 25, 40, 0.90)",
            "bordercolor": "rgba(255,255,255,0.25)",
        },
        "colorway": ["#8dd3c7", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5"],
        "xaxis": {"gridcolor": "rgba(255,255,255,0.12)", "zerolinecolor": "rgba(255,255,255,0.12)"},
        "yaxis": {"gridcolor": "rgba(255,255,255,0.12)", "zerolinecolor": "rgba(255,255,255,0.12)"},
    }
)

pio.templates["climate"] = climate_template
pio.templates.default = "climate"

# --- Styling (climate theme) -----------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

    /* Global font + background */
    .stApp {
        font-family: 'Rubik', sans-serif;
        font-size: 16px;
        background: linear-gradient(135deg, #08304c 0%, #0c5460 48%, #0f7a6a 100%);
        color: #f2f8ff;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(3, 37, 65, 0.95), rgba(7, 83, 96, 0.95));
        backdrop-filter: blur(18px);
        border-right: 1px solid rgba(255, 255, 255, 0.25);
        box-shadow: 4px 0 28px rgba(0, 0, 0, 0.45);
        min-height: 100vh;
        padding-top: 1.25rem;
        padding-bottom: 1.25rem;
    }

    section[data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }

    section[data-testid="stSidebar"] * {
        color: #f4faff;
    }

    /* Sidebar content should stretch to fill height so the footer can be positioned */
    section[data-testid="stSidebar"] > div {
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    section[data-testid="stSidebar"] .css-1d391kg {
        flex: 1;
    }

    /* Headers */
    .css-1v0mbdj h1,
    .css-1v0mbdj h2,
    .css-1v0mbdj h3 {
        color: #f2f8ff;
    }

    /* Tab styling */
    .css-1lcbmhc .stButton>button {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 12px;
        padding: 0.6rem 1.1rem;
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }

    .css-1lcbmhc .stButton>button:hover {
        background: rgba(255,255,255,0.18);
    }

    /* Chart / card styling */
    .css-1i0u1e2 {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 14px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
    }

    /* Key metric sizing */
    .stMetricValue {
        font-size: 2.6rem;
        font-weight: 800;
    }

    .stMetricLabel {
        color: rgba(255, 255, 255, 0.92);
        font-size: 1.3rem;
        font-weight: 700;
    }

    /* Increase overall text size where applicable */
    .stMarkdown, .stText, .stText span, .stCode {
        font-size: 1.2rem;
    }

    /* Slightly bigger sidebar labels */
    section[data-testid="stSidebar"] .stText,
    section[data-testid="stSidebar"] .stText span {
        font-size: 1.05rem;
    }

    .css-1v0mbdj h1 {
        font-size: 3.1rem !important;
        letter-spacing: 0.02em;
        margin-bottom: 0.2rem;
    }

    .css-1v0mbdj h2 {
        font-size: 2.1rem !important;
    }

    .css-1v0mbdj h3 {
        font-size: 1.75rem !important;
    }

    /* Insight box styling */
    .stAlert {
        border-left: 4px solid rgba(80, 180, 240, 0.85) !important;
        background: rgba(0, 0, 0, 0.25) !important;
        color: #f4fbff !important;
    }

    .stAlert p {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.9) !important;
    }

    /* Links */
    a {
        color: #80d4ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Data loading ------------------------------------------------------------
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

DATA_PATH = (
    Path(__file__).resolve().parents[0]
    / ".."
    / "untitled folder"
    / "global_weather_cleaned_daily.csv"
).resolve()

df = load_data(DATA_PATH)

# --- Sidebar (vertical menu) -----------------------------------------------
st.sidebar.title("Filters & KPIs")

country_options = ["All"] + sorted(df["country"].dropna().unique())
year_options = ["All"] + sorted(df["year"].dropna().unique())

selected_country = st.sidebar.selectbox("Country", country_options, index=0)
selected_year = st.sidebar.selectbox("Year", year_options, index=0)

filtered = df.copy()
if selected_country != "All":
    filtered = filtered[filtered["country"] == selected_country]
if selected_year != "All":
    filtered = filtered[filtered["year"] == selected_year]

st.sidebar.markdown("---")

avg_temp = filtered["temperature_celsius"].mean()
total_rain = filtered["precip_mm"].sum()
avg_wind = filtered["wind_kph"].mean()

extreme = filtered[
    (filtered["temperature_celsius"] > 40)
    | (filtered["precip_mm"] > 100)
    | (filtered["wind_kph"] > 60)
]

hottest_country = None
if not filtered.empty:
    hottest_country = (
        filtered.groupby("country")["temperature_celsius"].mean().idxmax()
    )

st.sidebar.markdown("### Key Metrics")

st.sidebar.metric("🌡 Avg Temp", round(avg_temp, 2))
st.sidebar.metric("🌧 Total Precip", round(total_rain, 2))
st.sidebar.metric("💨 Avg Wind", round(avg_wind, 2))

st.sidebar.markdown("---")

st.sidebar.metric("🚨 Extreme Events", len(extreme))
st.sidebar.metric("🔥 Hottest Country", hottest_country or "—")
st.sidebar.metric("Year", selected_year)

# Spacer so the sidebar fills the vertical height
st.sidebar.markdown("<div style='flex-grow:1'></div>", unsafe_allow_html=True)

# --- Horizontal menu (tabs) -----------------------------------------------
st.title("🌍 Global Climate Intelligence Dashboard")
st.markdown("<div id='top'></div>", unsafe_allow_html=True)

st.markdown(
    """
    Use the tabs below to explore different analytical views. The sidebar controls the global filters and displays key summary metrics.
    """
)

PAGES_DIR = Path(__file__).resolve().parent / "views"

# Load page modules on demand (keeps the app responsive)
# NOTE: We avoid streamlit caching here because module objects are not pickle-serializable.
from functools import lru_cache

@lru_cache(maxsize=32)
def load_page_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem.replace(" ", "_"), str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

page_files = sorted(PAGES_DIR.glob("*.py"))
page_labels = [p.stem.title() for p in page_files]

tabs = st.tabs(page_labels)

for tab, page_path in zip(tabs, page_files):
    with tab:
        module = load_page_module(page_path)
        if hasattr(module, "render"):
            module.render(filtered, selected_country, selected_year)
        else:
            st.warning(
                "This page does not expose a `render(df, selected_country, selected_year)` function."
            )


