"""
Climate Monitoring & Insights Dashboard  v5  (fully reviewed + fixed)
Run:  streamlit run global_weather_dashboard.py
Deps: streamlit plotly pandas numpy
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Global Weather Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
#  CONSTANTS
# ──────────────────────────────────────────────
DEFAULT_H    = 340
MONTH_ORDER  = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]
MMAP         = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
T_HEAT       = 40           # heatwave threshold °C
T_RAIN       = 25           # FIX BUG-004: heavy rain ≥25mm (WMO daily heavy-rain boundary)
T_WIND       = 16.67        # high wind threshold m/s (≈60 km/h)
WHO_PM25     = 15           # WHO PM2.5 guideline µg/m³
WHO_PM10     = 45           # WHO PM10 guideline µg/m³

# ──────────────────────────────────────────────
#  GLOBAL CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e8f4fd 0%, #dbeafe 20%, #ede9fe 50%, #d1fae5 80%, #fef9c3 100%);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
    min-height:100vh; font-family:'Inter',sans-serif;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
[data-testid="stHeader"]              { background:transparent !important; }
[data-testid="stMainBlockContainer"]  { background:transparent !important; }
[data-testid="stVerticalBlock"] > div { background:transparent !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f0f7ff 60%, #eef2ff 100%) !important;
    border-right: 2px solid #c7d2fe;
    box-shadow: 4px 0 20px rgba(99,102,241,0.10);
}
html, body, [class*="css"] { color:#1e293b; font-family:'Inter',sans-serif; }
h1,h2,h3 { color:#0f172a; }

.kpi-card {
    background-color: #1e293b;
    border: 1px solid rgba(0,0,0,0.15);
    border-radius: 16px;
    padding: 16px 20px 14px;
    backdrop-filter: blur(12px);
    height: 118px;
    display: flex; flex-direction: column; justify-content: space-between;
    cursor: default;
    transition: transform 0.25s cubic-bezier(.34,1.56,.64,1), box-shadow 0.25s ease;
    position: relative; overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.kpi-card::before {
    content:''; position:absolute; inset:0; border-radius:16px;
    background-color:rgba(255,255,255,0.05); opacity:0; transition:opacity 0.25s;
}
.kpi-card:hover { transform:translateY(-5px) scale(1.02); }
.kpi-card:hover::before { opacity:1; }

.kpi-label {
    font-size:10px; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; color:#ffffff !important; opacity:0.8;
}
.kpi-value {
    font-size:24px; font-weight:800; line-height:1.1;
    color:#ffffff !important; letter-spacing:-0.5px;
    overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}
.kpi-sub { font-size:11px; color:#ffffff !important; opacity:0.7; }

.kpi-cyan   { border-top:3px solid #00d4ff; }
.kpi-card.kpi-cyan:hover   { box-shadow:0 14px 44px rgba(0,212,255,0.4); }
.kpi-teal   { border-top:3px solid #00e5c0; }
.kpi-card.kpi-teal:hover   { box-shadow:0 14px 44px rgba(0,229,192,0.4); }
.kpi-purple { border-top:3px solid #a78bfa; }
.kpi-card.kpi-purple:hover { box-shadow:0 14px 44px rgba(167,139,250,0.4); }
.kpi-orange { border-top:3px solid #fb923c; }
.kpi-card.kpi-orange:hover { box-shadow:0 14px 44px rgba(251,146,60,0.4); }
.kpi-red    { border-top:3px solid #f87171; }
.kpi-card.kpi-red:hover    { box-shadow:0 14px 44px rgba(248,113,113,0.4); }
.kpi-yellow { border-top:3px solid #fbbf24; }
.kpi-card.kpi-yellow:hover { box-shadow:0 14px 44px rgba(251,191,36,0.4); }
.kpi-green  { border-top:3px solid #34d399; }
.kpi-card.kpi-green:hover  { box-shadow:0 14px 44px rgba(52,211,153,0.4); }
.kpi-blue   { border-top:3px solid #60a5fa; }
.kpi-card.kpi-blue:hover   { box-shadow:0 14px 44px rgba(96,165,250,0.4); }
.kpi-pink   { border-top:3px solid #f472b6; }
.kpi-card.kpi-pink:hover   { box-shadow:0 14px 44px rgba(244,114,182,0.4); }
.kpi-sky    { border-top:3px solid #38bdf8; }
.kpi-card.kpi-sky:hover    { box-shadow:0 14px 44px rgba(56,189,248,0.4); }

/* ── Tab base styles ── */
[data-testid="stTabs"] button {
    color:#64748b !important; font-size:12.5px; font-weight:700;
    letter-spacing:0.4px; padding:10px 16px; border-radius:8px 8px 0 0;
    border:2px solid #cbd5e1 !important; border-bottom:2px solid #cbd5e1 !important;
    background:#ffffff;
    transition:all 0.22s cubic-bezier(.34,1.56,.64,1); transform:translateY(0px);
    box-shadow:0 2px 6px rgba(0,0,0,0.06); margin:0 2px;
    white-space: nowrap;
}
[data-testid="stTabs"] button:hover {
    color:#0f172a !important; background:rgba(37,99,235,0.07) !important;
    border:2px solid #2563eb !important; border-bottom:2px solid #2563eb !important;
    box-shadow:0 -6px 18px rgba(37,99,235,0.18),0 2px 8px rgba(37,99,235,0.10);
    transform:translateY(-5px);
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color:#2563eb !important; background:rgba(37,99,235,0.10) !important;
    border:2px solid #2563eb !important; border-bottom:3px solid #2563eb !important;
    box-shadow:0 -4px 14px rgba(37,99,235,0.20),0 2px 8px rgba(37,99,235,0.10);
    transform:translateY(-3px);
}

/* ── Tab list: scrollable, no scrollbar ── */
[data-baseweb="tab-list"] {
    overflow-x: auto !important;
    overflow-y: visible !important;
    scroll-behavior: smooth !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
    flex-wrap: nowrap !important;
    display: flex !important;
    align-items: flex-end !important;
    padding-bottom: 2px !important;
    flex: 1 !important;
    min-width: 0 !important;
}
[data-baseweb="tab-list"]::-webkit-scrollbar {
    display: none !important;
}

.sec-hdr {
    font-size:13px; font-weight:800; letter-spacing:1.2px; text-transform:uppercase;
    margin-bottom:10px; padding-bottom:7px; border-bottom:1px solid rgba(0,0,0,0.1);
}
.hdr-cyan   { color:#0284c7; } .hdr-teal   { color:#0d9488; }
.hdr-red    { color:#dc2626; } .hdr-purple { color:#7c3aed; }
.hdr-orange { color:#ea580c; } .hdr-yellow { color:#ca8a04; }
.hdr-green  { color:#16a34a; } .hdr-blue   { color:#2563eb; }
.hdr-pink   { color:#db2777; }

.insight-box {
    background:linear-gradient(135deg,rgba(56,189,248,0.1),rgba(52,211,153,0.1));
    border:1px solid rgba(56,189,248,0.3); border-left:4px solid #0ea5e9;
    border-radius:10px; padding:13px 17px; font-size:13px;
    color:#0f172a; margin-bottom:16px; font-weight:500;
}
.alert-box {
    background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3);
    border-left:4px solid #ef4444; border-radius:8px;
    padding:9px 15px; font-size:13px; color:#991b1b; margin-bottom:12px; font-weight:600;
}
.ok-box {
    background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.3);
    border-left:4px solid #22c55e; border-radius:8px;
    padding:9px 15px; font-size:13px; color:#166534; margin-bottom:12px; font-weight:600;
}

[data-testid="stSidebar"],
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] b,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] .stMarkdown { color:#000000 !important; }
[data-testid="stSidebar"] label { font-size:11.5px; font-weight:700; letter-spacing:0.8px; }

[data-testid="stSelectbox"] div,
div[data-baseweb="select"] > div,
div[data-baseweb="select"] span { color:#000000 !important; }
div[data-baseweb="select"] > div { background-color:white !important; }
div[data-baseweb="popover"] ul  { background-color:white !important; }
div[data-baseweb="popover"] li  { background-color:white !important; color:#000000 !important; }
div[data-baseweb="popover"] li:hover { background-color:#f0f0f0 !important; }

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] *,
.element-container p,
.stMarkdown p,
caption { color:#000000 !important; }

[data-testid="stPlotlyChart"] {
    border:2.5px solid rgba(99,102,241,0.25) !important;
    border-radius:18px !important; padding:12px 8px 6px 8px !important;
    background:rgba(255,255,255,0.82) !important; backdrop-filter:blur(12px) !important;
    box-shadow:0 4px 24px rgba(99,102,241,0.10),0 1px 4px rgba(0,0,0,0.05) !important;
    transition:all 0.28s cubic-bezier(.34,1.56,.64,1);
}
[data-testid="stPlotlyChart"]:hover {
    border-color:#6366f1 !important; background:rgba(255,255,255,0.96) !important;
    box-shadow:0 8px 36px rgba(99,102,241,0.22),0 2px 8px rgba(0,0,0,0.08) !important;
    transform:translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  TAB NAVIGATION ARROWS (Previous / Next tab)
#  Uses components.html so JS actually executes.
#  height=0 keeps it invisible in the layout.
# ──────────────────────────────────────────────
components.html("""
<style>
  /* These styles are injected into the PARENT frame via the JS below */
</style>
<script>
(function () {
    'use strict';

    /* ── reach into the Streamlit parent document ── */
    var doc = window.parent.document;

    /* ── button CSS injected once into parent <head> ── */
    function injectCSS() {
        if (doc.getElementById('tab-nav-style')) return;
        var s = doc.createElement('style');
        s.id = 'tab-nav-style';
        s.textContent = [
            '.tab-nav-wrapper{display:flex!important;align-items:center!important;',
            'width:100%!important;min-width:0!important;overflow:visible!important;}',

            '[data-baseweb="tab-list"]{overflow-x:auto!important;overflow-y:visible!important;',
            'scroll-behavior:smooth!important;scrollbar-width:none!important;',
            '-ms-overflow-style:none!important;flex-wrap:nowrap!important;',
            'display:flex!important;align-items:flex-end!important;',
            'padding-bottom:2px!important;flex:1!important;min-width:0!important;}',

            '[data-baseweb="tab-list"]::-webkit-scrollbar{display:none!important;}',

            '.tab-nav-btn{flex-shrink:0;width:36px;height:40px;',
            'border:2px solid #cbd5e1;border-radius:10px;',
            'background:linear-gradient(135deg,#fff 0%,#f8faff 100%);',
            'color:#2563eb;font-size:20px;font-weight:800;cursor:pointer;',
            'display:flex;align-items:center;justify-content:center;',
            'box-shadow:0 2px 8px rgba(37,99,235,.12);',
            'transition:all .2s cubic-bezier(.34,1.56,.64,1);',
            'z-index:9999;user-select:none;line-height:1;padding:0;',
            'align-self:center;}',

            '.tab-nav-btn:hover{background:rgba(37,99,235,.08);border-color:#2563eb;',
            'box-shadow:0 0 0 3px rgba(37,99,235,.15),0 4px 16px rgba(37,99,235,.25);',
            'transform:translateY(-2px) scale(1.08);color:#1d4ed8;}',

            '.tab-nav-btn:active{transform:scale(.95);}',

            '.tab-nav-btn.tn-disabled{opacity:.25;cursor:not-allowed;pointer-events:none;}',

            '.tab-nav-btn.prev-btn{margin-right:6px;}',
            '.tab-nav-btn.next-btn{margin-left:6px;}'
        ].join('');
        doc.head.appendChild(s);
    }

    /* ── helpers ── */
    function getTabBtns(tabList) {
        return Array.from(tabList.querySelectorAll('button[role="tab"]'));
    }

    function getActiveIdx(btns) {
        for (var i = 0; i < btns.length; i++) {
            if (btns[i].getAttribute('aria-selected') === 'true') return i;
        }
        return 0;
    }

    function scrollIntoView(tabList, btn) {
        var L = btn.offsetLeft, R = L + btn.offsetWidth;
        var sL = tabList.scrollLeft, sR = sL + tabList.clientWidth;
        if (L < sL + 8)  tabList.scrollTo({left: L - 8,                        behavior:'smooth'});
        else if (R > sR - 8) tabList.scrollTo({left: R - tabList.clientWidth + 8, behavior:'smooth'});
    }

    /* ── main injection ── */
    function inject() {
        injectCSS();
        var tabLists = doc.querySelectorAll('[data-baseweb="tab-list"]');

        tabLists.forEach(function (tabList) {
            if (tabList.parentElement && tabList.parentElement.classList.contains('tab-nav-wrapper')) return;

            /* wrap */
            var wrap = doc.createElement('div');
            wrap.className = 'tab-nav-wrapper';
            tabList.parentNode.insertBefore(wrap, tabList);
            wrap.appendChild(tabList);
            tabList.style.flex = '1';
            tabList.style.minWidth = '0';

            /* buttons */
            var prev = doc.createElement('button');
            prev.className = 'tab-nav-btn prev-btn';
            prev.innerHTML = '&#8592;';
            prev.title = 'Previous tab';

            var next = doc.createElement('button');
            next.className = 'tab-nav-btn next-btn';
            next.innerHTML = '&#8594;';
            next.title = 'Next tab';

            wrap.insertBefore(prev, tabList);
            wrap.appendChild(next);

            /* update disabled */
            function upd() {
                var btns = getTabBtns(tabList);
                var idx  = getActiveIdx(btns);
                prev.classList.toggle('tn-disabled', idx <= 0);
                next.classList.toggle('tn-disabled', idx >= btns.length - 1);
                if (btns[idx-1]) prev.title = '\u2190 ' + btns[idx-1].textContent.trim();
                if (btns[idx+1]) next.title = btns[idx+1].textContent.trim() + ' \u2192';
            }

            /* click: switch tab */
            prev.addEventListener('click', function (e) {
                e.preventDefault(); e.stopPropagation();
                var btns = getTabBtns(tabList), idx = getActiveIdx(btns);
                if (idx > 0) { btns[idx-1].click(); setTimeout(function(){ scrollIntoView(tabList,btns[idx-1]); upd(); },80); }
            });
            next.addEventListener('click', function (e) {
                e.preventDefault(); e.stopPropagation();
                var btns = getTabBtns(tabList), idx = getActiveIdx(btns);
                if (idx < btns.length-1) { btns[idx+1].click(); setTimeout(function(){ scrollIntoView(tabList,btns[idx+1]); upd(); },80); }
            });

            /* watch aria-selected changes */
            tabList.addEventListener('click', function(){ setTimeout(upd, 120); });
            new MutationObserver(upd).observe(tabList, {attributes:true, subtree:true, attributeFilter:['aria-selected']});

            upd();
            setTimeout(upd, 500);
        });
    }

    /* ── poll until tabs are rendered ── */
    var tries = 0;
    var poll = setInterval(function () {
        var tl = doc.querySelector('[data-baseweb="tab-list"]');
        if (tl && tl.querySelectorAll('button[role="tab"]').length > 0) {
            inject();
            clearInterval(poll);
        }
        if (++tries > 60) clearInterval(poll);
    }, 150);

    /* ── re-inject on full Streamlit rerenders ── */
    new MutationObserver(function (muts) {
        muts.forEach(function (m) {
            m.addedNodes.forEach(function (n) {
                if (n.nodeType === 1 && n.querySelector && n.querySelector('[data-baseweb="tab-list"]')) {
                    setTimeout(inject, 200);
                }
            });
        });
    }).observe(doc.body, {childList:true, subtree:true});

})();
</script>
""", height=0)


# ──────────────────────────────────────────────
#  DATA LOADING  (cached)
# ──────────────────────────────────────────────
@st.cache_data
def load_data():
    # FIX BUG-010: graceful error on missing CSV
    try:
        df = pd.read_csv("cleaned_global_weather_monthly.csv")
    except FileNotFoundError:
        st.error(
            "⚠️ Data file not found.\n\n"
            "Place **`cleaned_global_weather_monthly.csv`** in the same directory as this app and reload."
        )
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Failed to load data: {e}")
        st.stop()

    df["month_name"] = pd.Categorical(
        pd.to_datetime(df["month"], format="%m").dt.strftime("%b"),
        categories=MONTH_ORDER, ordered=True,
    )
    return df


# FIX BUG-002: pass df as argument so @st.cache_data can hash it correctly.
@st.cache_data
def compute_monthly_agg(df, country, year):
    """Monthly averages for the selected country+year combination."""
    mask = df["year"] == year
    if country != "All Countries":
        mask &= df["country"] == country
    sub = df[mask]
    return (
        sub.groupby(["month", "month_name"], observed=True)
        .agg(
            temp    =("temperature_celsius", "mean"),
            precip  =("precip_mm",           "mean"),
            wind    =("wind_mps",             "mean"),
            humidity=("humidity",             "mean"),
            cloud   =("cloud",                "mean"),
            uv      =("uv_index",             "mean"),
            pm25    =("air_quality_PM2.5",    "mean"),
            pm10    =("air_quality_PM10",     "mean"),
        )
        .reset_index()
        .sort_values("month")
    )

# FIX BUG-003: pass df as argument so @st.cache_data can hash it correctly.
# FIX BUG-005: unified cold-stress term — single source of truth for risk scoring.
@st.cache_data
def compute_risk_scores(df, year):
    """Vectorised risk score for every row in a given year (fast, single formula)."""
    sub = df[df["year"] == year].copy()
    sub["Risk"] = (
        ((sub["temperature_celsius"] > 35).astype(int) * 30) +
        (((sub["temperature_celsius"] > 30) &
          (sub["temperature_celsius"] <= 35)).astype(int) * 15) +
        ((sub["precip_mm"] > 10).astype(int) * 25) +
        ((sub["precip_mm"] < 0.5).astype(int) * 15) +
        ((sub["wind_mps"] > 15).astype(int) * 20) +
        ((sub["uv_index"] > 8).astype(int) * 15) +
        ((sub["air_quality_PM2.5"] > 25).astype(int) * 10) +
        ((sub["temperature_celsius"] < 0).astype(int) * 20)  # cold-stress
    ).clip(upper=100)
    return sub


# FIX PERF-001: cache the top-N treemap aggregations keyed on year.
@st.cache_data
def compute_top30_temp(df, year):
    return df[df["year"] == year].groupby("country")["temperature_celsius"].mean().nlargest(30).reset_index()

@st.cache_data
def compute_top40_risk(df, year):
    scored = compute_risk_scores(df, year)
    return scored.groupby("country")["Risk"].mean().nlargest(40).reset_index()


# ──────────────────────────────────────────────
#  PLOTLY SHARED DEFAULTS
# ──────────────────────────────────────────────
PBG = "rgba(0,0,0,0)"
GRD = "rgba(0,0,0,0.06)"
AXC = "rgba(0,0,0,0.25)"
HVR = dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="rgba(0,0,0,0.2)",
           font=dict(color="#0f172a", size=12))
_AX = dict(
    gridcolor=GRD, linecolor=AXC, zerolinecolor=AXC,
    tickfont=dict(color="#000000", size=11, family="Inter"),
    title_font=dict(color="#000000", size=12, family="Inter"),
    tickcolor="#000000", color="#000000",
)

def BL(accent="#2563eb", h=DEFAULT_H, title="", **kw):
    return dict(
        paper_bgcolor=PBG, plot_bgcolor=PBG,
        font=dict(color="#000000", size=12),
        margin=dict(l=44, r=24, t=46, b=44),
        title=dict(text=title,
                   font=dict(color=accent, size=13, family="Inter", weight="bold"), x=0.01),
        xaxis=_AX.copy(), yaxis=_AX.copy(),
        legend=dict(bgcolor="rgba(255,255,255,0.7)", bordercolor="rgba(0,0,0,0.1)",
                    borderwidth=1, font=dict(color="#000000")),
        hoverlabel=HVR, height=h, **kw,
    )


# ──────────────────────────────────────────────
#  HELPER FUNCTIONS
# ──────────────────────────────────────────────
def kpi(label, value, sub, cls):
    return (
        f"<div class='kpi-card {cls}'>"
        f"<div class='kpi-label'>{label}</div>"
        f"<div class='kpi-value' title='{value}'>{value}</div>"
        f"<div class='kpi-sub'>{sub}</div></div>"
    )

def sh(text, cls="hdr-cyan"):
    return f"<div class='sec-hdr {cls}'>{text}</div>"

def safe_idxmax(series):
    return series.idxmax() if len(series) and series.notna().any() else "N/A"

def safe_max(series, default=0):
    return series.max() if len(series) else default

def safe_mean(series, default=0):
    return series.mean() if len(series) else default

def truncate_label(name, max_len=18):
    return name if len(name) <= max_len else name[:max_len - 1] + "…"

def ensure_full_months(series_or_df, value_col=None):
    if isinstance(series_or_df, pd.Series):
        return series_or_df.reindex(MONTH_ORDER, fill_value=0)
    full_idx = pd.CategoricalIndex(MONTH_ORDER, categories=MONTH_ORDER, ordered=True)
    return (
        series_or_df
        .set_index("month_name")
        .reindex(full_idx, fill_value=0)
        .reset_index()
    )

def highlight_country(fig, country, df_c=None, col=None, label=None,
                      fmt=".2f", line_width=2.0):
    if not country or country == "All Countries":
        return fig

    for trace in fig.data:
        if trace.type == "choropleth":
            trace.marker.opacity       = 0.15
            trace.marker.line.color    = "rgba(255,255,255,0.08)"
            trace.marker.line.width    = 0.1
            trace.hovertemplate        = ""
            trace.hoverinfo            = "skip"

    actual_value = None
    hover_text   = f"<b>{country}</b> ★ Selected"

    # FIX BUG-009: case-insensitive country name lookup
    if df_c is not None and col is not None and label is not None:
        row = df_c[df_c["country"].str.lower() == country.lower()]
        if not row.empty:
            actual_value = float(row.iloc[0][col])
            hover_text   = (
                f"<b>{country}</b> ★ Selected"
                f"<br>{label}: <b>{actual_value:{fmt}}</b>"
            )

    base_z    = None
    base_zmin = None
    base_zmax = None
    for trace in fig.data:
        if trace.type == "choropleth" and trace.z is not None:
            base_z    = list(trace.z)
            base_zmin = min(base_z)
            base_zmax = max(base_z)
            break

    z_val = actual_value if actual_value is not None else (base_zmax or 100)

    fig.add_trace(go.Choropleth(
        locations=[country],
        locationmode="country names",
        z=[z_val],
        zmin=base_zmin, zmax=base_zmax,
        showscale=False,
        colorscale=[[0.0, "#FFB800"], [0.5, "#FFD700"], [1.0, "#FFE44D"]],
        marker=dict(line=dict(color="#D97706", width=line_width), opacity=1.0),
        hovertemplate=hover_text + "<extra></extra>",
        showlegend=False,
        name="",
    ))
    return fig


def make_choropleth(df_c, col, color_scale, title, accent, label, year,
                    sel_country="All Countries", fmt=".2f"):
    fig = px.choropleth(
        df_c, locations="country", locationmode="country names",
        color=col, color_continuous_scale=color_scale, labels={col: label},
    )
    fig.update_traces(
        hovertemplate=f"<b>%{{location}}</b><br>{label}: %{{z:{fmt}}}<extra></extra>",
        marker_line_color="#ffffff", marker_line_width=0.3,
    )
    fig.update_geos(
        showframe=False, showcoastlines=True, coastlinecolor="#cbd5e1",
        showland=True, landcolor="#f1f5f9", showocean=True, oceancolor="#e0f2fe",
        projection_type="natural earth",
    )
    fig.update_layout(
        paper_bgcolor=PBG, plot_bgcolor=PBG, hoverlabel=HVR,
        geo=dict(bgcolor=PBG), height=420, margin=dict(l=0, r=0, t=40, b=0),
        font=dict(color="#000000"),
        coloraxis_colorbar=dict(
            title=dict(text=label, font=dict(color="#000000")),
            tickfont=dict(color="#000000"), bgcolor="rgba(255,255,255,0.7)",
        ),
        title=dict(text=f"{title} · {year}",
                   font=dict(color=accent, size=13, weight="bold"), x=0.01),
    )
    highlight_country(fig, sel_country, df_c=df_c, col=col, label=label, fmt=fmt)
    return fig


# ──────────────────────────────────────────────
#  LOAD DATA
# ──────────────────────────────────────────────
df_full = load_data()


# ──────────────────────────────────────────────
#  SIDEBAR  — FIX UX-001: use proper selectbox labels for accessibility
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 22px'>
        <div style='font-size:36px'>🌍</div>
        <div style='font-size:15px;font-weight:800;color:#0f172a;letter-spacing:1.5px'>WEATHER IQ</div>
        <div style='font-size:9.5px;color:#475569;letter-spacing:3px;margin-top:3px'>INTELLIGENCE DASHBOARD</div>
    </div>
    <hr style='border:1px solid #cbd5e1;margin-bottom:22px'>
    """, unsafe_allow_html=True)

    # FIX UX-001: native selectbox labels instead of hidden markdown headers
    countries   = ["All Countries"] + sorted(df_full["country"].unique().tolist())
    sel_country = st.selectbox("🌐 Country", countries)

    years    = sorted(df_full["year"].unique().tolist())
    sel_year = st.selectbox("📅 Year", years)

    n_c  = len(df_full["country"].unique())
    ystr = f"{df_full['year'].min()} – {df_full['year'].max()}"


# ──────────────────────────────────────────────
#  FILTERED DATA
# ──────────────────────────────────────────────
df_year     = df_full[df_full["year"] == sel_year].copy()
df_filtered = (
    df_year[df_year["country"] == sel_country].copy()
    if sel_country != "All Countries" else df_year.copy()
)

# FIX BUG-002/003: pass df_full into cached helpers
df_monthly  = compute_monthly_agg(df_full, sel_country, sel_year)
scope       = sel_country if sel_country != "All Countries" else "Global"

# Year-over-year anomaly
df_prev = df_full[df_full["year"] == sel_year - 1]
if sel_country != "All Countries":
    df_prev = df_prev[df_prev["country"] == sel_country]
prev_avg_t = safe_mean(df_prev["temperature_celsius"], default=None) if len(df_prev) else None
curr_avg_t = safe_mean(df_filtered["temperature_celsius"])
anomaly    = float(curr_avg_t - prev_avg_t) if prev_avg_t is not None else 0.0

# FIX BUG-003: pass df_full
df_year_risk = compute_risk_scores(df_full, sel_year)

# ──────────────────────────────────────────────
#  GUARD: no data for selected combination
# ──────────────────────────────────────────────
if df_monthly.empty:
    st.warning(f"⚠️ No monthly data available for **{scope}** in **{sel_year}**. Try a different year or country.")
    st.stop()


# ──────────────────────────────────────────────
#  HEADER
# ──────────────────────────────────────────────
st.markdown(f"""
<div style='
    background:linear-gradient(135deg,#ffffff 0%,#eff6ff 50%,#f0fdf4 100%);
    border:2px solid #e2e8f0; border-radius:20px;
    padding:24px 32px; margin-bottom:24px;
    box-shadow:0 4px 24px rgba(37,99,235,0.08),0 1px 4px rgba(0,0,0,0.04);
    position:relative; overflow:hidden;
'>
  <div style='position:absolute;top:0;left:0;right:0;height:4px;
              background:linear-gradient(90deg,#2563eb,#0ea5e9,#10b981);
              border-radius:20px 20px 0 0;'></div>
  <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;margin-top:6px;'>
    <div style='display:flex;align-items:center;gap:16px;'>
      <div style='background:linear-gradient(135deg,#2563eb,#0ea5e9);
                  border-radius:16px;padding:12px 14px;font-size:30px;line-height:1;
                  box-shadow:0 4px 14px rgba(37,99,235,0.30);'>🌍</div>
      <div>
        <div style='font-size:22px;font-weight:900;color:#0f172a;'>
          Climate Monitoring &amp; Insights Dashboard
        </div>
        <div style='font-size:12px;color:#64748b;margin-top:6px;font-weight:500;display:flex;align-items:center;gap:8px;'>
          <span style='background:#eff6ff;border:1px solid #bfdbfe;border-radius:20px;
                       padding:2px 10px;color:#2563eb;font-weight:700;font-size:11px;'>🌐 Climate Analytics</span>
          <span style='background:#f0fdf4;border:1px solid #bbf7d0;border-radius:20px;
                       padding:2px 10px;color:#16a34a;font-weight:700;font-size:11px;'>📊 {n_c} Countries</span>
          <span style='background:#fefce8;border:1px solid #fde68a;border-radius:20px;
                       padding:2px 10px;color:#ca8a04;font-weight:700;font-size:11px;'>📅 {ystr}</span>
        </div>
      </div>
    </div>
    <div style='background:linear-gradient(135deg,#2563eb,#0ea5e9);
                border-radius:30px;padding:10px 22px;
                box-shadow:0 4px 14px rgba(37,99,235,0.25);
                display:flex;align-items:center;gap:10px;'>
      <span style='font-size:16px;'>📍</span>
      <span style='font-size:14px;color:#ffffff;font-weight:800;'>{scope}</span>
      <span style='width:6px;height:6px;background:rgba(255,255,255,0.5);border-radius:50%;display:inline-block;'></span>
      <span style='font-size:14px;color:rgba(255,255,255,0.85);font-weight:700;'>{sel_year}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  TABS
# ──────────────────────────────────────────────
tabs = st.tabs([
    "🌐 Executive Overview",
    "🌡 Temperature",
    "🌧 Precipitation & Wind",
    "🚨 Extreme Events",
    "🏆 Regional Comparison",
    "💧 Humidity & Cloud",
    "☀️ UV & Air Quality",
    "⚠️ Climate Risk",
])


# ════════════════════════════════════════════════
#  TAB 1 — EXECUTIVE OVERVIEW
# ════════════════════════════════════════════════
with tabs[0]:
    avg_t = safe_mean(df_filtered["temperature_celsius"])

    # FIX BUG-006: for multi-country selections use mean monthly precip, not raw sum
    if sel_country == "All Countries":
        precip_display = safe_mean(df_filtered["precip_mm"])
        precip_label   = "avg monthly (mm)"
    else:
        precip_display = df_filtered["precip_mm"].sum() if len(df_filtered) else 0
        precip_label   = "annual total (mm)"

    avg_w = safe_mean(df_filtered["wind_mps"])
    n_ext = int(
        ((df_filtered["temperature_celsius"] > T_HEAT) |
         (df_filtered["precip_mm"] > T_RAIN) |
         (df_filtered["wind_mps"] > T_WIND)).sum()
    ) if len(df_filtered) else 0

    hot_series = df_year.groupby("country")["temperature_celsius"].mean()
    hot_c = safe_idxmax(hot_series)
    hot_v = safe_max(hot_series)
    a_str = (f"{'▲' if anomaly >= 0 else '▼'} {abs(anomaly):.2f}°C vs {sel_year-1}"
             if prev_avg_t is not None else "N/A")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: st.markdown(kpi("🌡 Avg Temp",    f"{avg_t:.1f}°C", scope,                  "kpi-cyan"),    unsafe_allow_html=True)
    with c2: st.markdown(kpi("📈 Anomaly",     a_str,           "YoY change",            "kpi-orange"),  unsafe_allow_html=True)
    with c3: st.markdown(kpi("🌧 Precipitation",f"{precip_display:.1f}mm", precip_label, "kpi-blue"),    unsafe_allow_html=True)
    with c4: st.markdown(kpi("💨 Avg Wind",    f"{avg_w:.2f}m/s","mean speed",           "kpi-teal"),    unsafe_allow_html=True)
    with c5: st.markdown(kpi("🚨 Extreme Evts",str(n_ext),      "breaches",              "kpi-red"),     unsafe_allow_html=True)
    with c6: st.markdown(kpi("🔥 Hottest",     truncate_label(hot_c), f"{hot_v:.1f}°C",  "kpi-yellow"),  unsafe_allow_html=True)

    st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""<div class='insight-box'>💡 <b>Snapshot {sel_year}:</b> {scope} averaged
        <b>{avg_t:.1f}°C</b>, precipitation <b>{precip_display:.1f}mm</b> ({precip_label}), avg wind
        <b>{avg_w:.2f}m/s</b>. <b>{n_ext}</b> extreme threshold breaches recorded.</div>""",
        unsafe_allow_html=True,
    )

    col_l, col_r = st.columns(2)

    with col_l:
        hm_df = (
            df_year.groupby("country").agg(
                Temperature  =("temperature_celsius", "mean"),
                Precipitation=("precip_mm",           "mean"),
                Wind         =("wind_mps",             "mean"),
                Humidity     =("humidity",             "mean"),
                UV_Index     =("uv_index",             "mean"),
                PM25         =("air_quality_PM2.5",    "mean"),
            )
            .reset_index()
            .nlargest(20, "Temperature")
            .set_index("country")
        )
        hm_norm = hm_df.apply(
            lambda col: (col - col.min()) / (col.max() - col.min() + 1e-9) * 100, axis=0
        ).round(1)
        hm_norm.columns = ["🌡 Temp","🌧 Precip","💨 Wind","💧 Humidity","☀️ UV","🌫 PM2.5"]
        fig1 = px.imshow(
            hm_norm.T,
            color_continuous_scale=["#eff6ff","#93c5fd","#3b82f6","#f59e0b","#ef4444","#7f1d1d"],
            aspect="auto", text_auto=".0f", labels=dict(color="Score (0–100)"),
        )
        fig1.update_traces(
            hovertemplate="<b>%{y}</b> · <b>%{x}</b><br>Score: %{z:.0f}/100<extra></extra>",
            textfont=dict(size=9, color="#000000"),
        )
        fig1.update_layout(**BL("#ea580c", DEFAULT_H, f"Climate Fingerprint — Top 20 Countries · {scope}"))
        fig1.update_xaxes(tickfont=dict(color="#000000", size=10), tickangle=-35)
        fig1.update_yaxes(tickfont=dict(color="#000000", size=11))
        fig1.update_coloraxes(colorbar=dict(
            title=dict(text="Score", font=dict(color="#000000")),
            tickfont=dict(color="#000000"),
        ))
        st.plotly_chart(fig1, use_container_width=True)

    with col_r:
        # FIX PERF-001: use cached aggregation
        top30 = compute_top30_temp(df_full, sel_year)
        fig2  = px.treemap(
            top30, path=["country"], values="temperature_celsius",
            color="temperature_celsius",
            color_continuous_scale=["#3b82f6","#eab308","#f97316","#ef4444","#991b1b"],
        )
        fig2.update_traces(
            textfont=dict(color="#ffffff", size=12, family="Inter", weight="bold"),
            hovertemplate="<b>%{label}</b><br>Avg Temp: %{color:.1f}°C<extra></extra>",
        )
        fig2.update_layout(**BL("#0d9488", DEFAULT_H, "Top 30 Countries — Avg Temperature Treemap"))
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        trends = df_monthly[["month_name","temp","precip","wind","humidity","uv","pm25"]].copy()
        fig3 = go.Figure()
        for col_name, label, clr in [
            ("temp",     "🌡 Temp",     "#ef4444"),
            ("humidity", "💧 Humidity", "#3b82f6"),
            ("uv",       "☀️ UV",       "#f59e0b"),
            ("wind",     "💨 Wind",     "#10b981"),
            ("precip",   "🌧 Precip",   "#06b6d4"),
            ("pm25",     "🌫 PM2.5",    "#8b5cf6"),
        ]:
            mn, mx = trends[col_name].min(), trends[col_name].max()
            norm   = ((trends[col_name] - mn) / (mx - mn + 1e-9) * 100).round(1)
            fig3.add_trace(go.Scatter(
                x=trends["month_name"], y=norm, mode="lines+markers", name=label,
                line=dict(color=clr, width=2), marker=dict(size=6, color=clr),
                hovertemplate=f"<b>%{{x}}</b><br>{label}: %{{customdata:.2f}}<extra></extra>",
                customdata=trends[col_name],
            ))
        fig3.update_layout(**BL("#7c3aed", DEFAULT_H, f"All Metrics Monthly Normalised Trend · {scope}"))
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["humidity"],
            mode="lines", fill="tozeroy", name="💧 Humidity (%)",
            line=dict(color="#3b82f6", width=2), fillcolor="rgba(59,130,246,0.15)",
            hovertemplate="<b>%{x}</b><br>Humidity: %{y:.1f}%<extra></extra>",
        ))
        fig4.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["cloud"],
            mode="lines", fill="tonexty", name="☁️ Cloud (%)",
            line=dict(color="#06b6d4", width=2), fillcolor="rgba(6,182,212,0.15)",
            hovertemplate="<b>%{x}</b><br>Cloud: %{y:.1f}%<extra></extra>",
        ))
        fig4.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["uv"] * 10,
            mode="lines+markers", name="☀️ UV ×10",
            line=dict(color="#f59e0b", width=2.5, dash="dot"),
            marker=dict(size=6, color="#f59e0b"),
            hovertemplate="<b>%{x}</b><br>UV Index: %{customdata:.1f}<extra></extra>",
            customdata=df_monthly["uv"],
        ))
        fig4.update_layout(**BL("#0d9488", DEFAULT_H, f"Monthly Humidity · Cloud · UV Overlay · {scope}"))
        st.plotly_chart(fig4, use_container_width=True)

    col_l3, col_r3 = st.columns(2)

    with col_l3:
        ht_df = df_year.groupby("country").agg(
            temp    =("temperature_celsius", "mean"),
            humidity=("humidity",            "mean"),
            precip  =("precip_mm",           "mean"),
        ).reset_index()
        fig5 = px.scatter(
            ht_df, x="temp", y="humidity", color="precip", hover_name="country",
            color_continuous_scale=["#fef9c3","#06b6d4","#1d4ed8"],
            labels={"temp":"Avg Temp (°C)","humidity":"Avg Humidity (%)","precip":"Precip (mm)"},
        )
        fig5.update_traces(
            marker=dict(size=9, opacity=0.85, line=dict(width=1, color="#ffffff")),
            hovertemplate="<b>%{hovertext}</b><br>Temp: %{x:.1f}°C<br>Humidity: %{y:.1f}%<extra></extra>",
        )
        fig5.update_layout(**BL("#0284c7", DEFAULT_H, "Humidity vs Temperature — All Countries"))
        fig5.update_coloraxes(colorbar=dict(
            title=dict(text="Precip", font=dict(color="#000000")),
            tickfont=dict(color="#000000"),
        ))
        st.plotly_chart(fig5, use_container_width=True)

    with col_r3:
        fig6 = make_subplots(specs=[[{"secondary_y": True}]])
        fig6.add_trace(go.Bar(
            x=df_monthly["month_name"], y=df_monthly["temp"],
            name="Avg Temp (°C)", marker_color="#0284c7", opacity=0.85,
            hovertemplate="<b>%{x}</b><br>Temp: %{y:.1f}°C<extra></extra>",
        ), secondary_y=False)
        fig6.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["precip"],
            name="Precip (mm)", mode="lines+markers",
            line=dict(color="#0d9488", width=3),
            marker=dict(size=8, color="#0d9488", line=dict(width=1.5, color="#ffffff")),
            hovertemplate="<b>%{x}</b><br>Precip: %{y:.2f}mm<extra></extra>",
        ), secondary_y=True)
        fig6.update_layout(**BL("#0284c7", DEFAULT_H, f"Monthly Avg Temperature & Precipitation · {scope}"))
        for ax_kw, sec in [("Temp (°C)", False), ("Precip (mm)", True)]:
            fig6.update_yaxes(
                title_text=ax_kw, secondary_y=sec,
                gridcolor=GRD if not sec else "rgba(0,0,0,0)",
                linecolor=AXC, tickfont=dict(color="#000000"),
                title_font=dict(color="#000000"),
            )
        st.plotly_chart(fig6, use_container_width=True)


# ════════════════════════════════════════════════
#  TAB 2 — TEMPERATURE INTELLIGENCE
# ════════════════════════════════════════════════
with tabs[1]:
    avg_t  = safe_mean(df_filtered["temperature_celsius"])
    max_t  = df_filtered["temperature_celsius"].max() if len(df_filtered) else 0
    min_t  = df_filtered["temperature_celsius"].min() if len(df_filtered) else 0
    rng_t  = max_t - min_t
    max_tc = (df_filtered.loc[df_filtered["temperature_celsius"].idxmax(), "country"]
              if len(df_filtered) else "N/A")
    min_tc = (df_filtered.loc[df_filtered["temperature_celsius"].idxmin(), "country"]
              if len(df_filtered) else "N/A")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi("🌡 Avg Temp",  f"{avg_t:.1f}°C", scope,                  "kpi-orange"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("🔥 Max Temp",  f"{max_t:.1f}°C", truncate_label(max_tc), "kpi-red"),    unsafe_allow_html=True)
    with c3: st.markdown(kpi("🧊 Min Temp",  f"{min_t:.1f}°C", truncate_label(min_tc), "kpi-blue"),   unsafe_allow_html=True)
    with c4: st.markdown(kpi("📏 Range",     f"{rng_t:.1f}°C", "max − min",            "kpi-purple"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("📈 Anomaly",   f"{anomaly:+.2f}°C", f"vs {sel_year-1}",  "kpi-yellow"), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
    bx = "alert-box" if anomaly > 1.5 else "ok-box"
    bm = (f"🔴 High Heat Anomaly: +{anomaly:.2f}°C above prior year"
          if anomaly > 1.5
          else f"✅ Temperature anomaly ({anomaly:+.2f}°C) is within stable margins.")
    st.markdown(f"<div class='{bx}'>{bm}</div>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        dv = df_year.copy()
        dv["mn"] = pd.Categorical(dv["month"].map(MMAP), categories=MONTH_ORDER, ordered=True)
        violin_title = f"Monthly Temp Distribution — All Countries · {sel_year}"
        fig = px.violin(
            dv, x="mn", y="temperature_celsius", color="mn", box=True, points="outliers",
            color_discrete_sequence=px.colors.sequential.Oranges_r,
            labels={"mn":"Month","temperature_celsius":"Temp (°C)"},
            category_orders={"mn": MONTH_ORDER},
        )
        fig.update_traces(
            selector=dict(type="violin"),
            hovertemplate="<b>%{x}</b><br>Temp: %{y:.1f}°C<extra></extra>",
        )
        if sel_country != "All Countries":
            violin_title = f"Monthly Temp Distribution — {sel_country} avg ◆ on global · {sel_year}"
            country_avg = (
                df_year[df_year["country"] == sel_country]
                .groupby("month")["temperature_celsius"].mean()
                .reset_index()
            )
            country_avg["mn"] = pd.Categorical(
                country_avg["month"].map(MMAP), categories=MONTH_ORDER, ordered=True
            )
            country_avg = country_avg.sort_values("mn")
            fig.add_trace(go.Scatter(
                x=country_avg["mn"], y=country_avg["temperature_celsius"],
                mode="markers+lines", name=f"{sel_country} avg",
                marker=dict(size=14, color="#0f172a", symbol="diamond",
                            line=dict(color="#ffffff", width=2)),
                line=dict(color="#0f172a", width=1.5, dash="dot"),
                hovertemplate=f"<b>{sel_country}</b> · %{{x}}<br>Avg: %{{y:.1f}}°C<extra></extra>",
            ))
            fig.update_layout(**BL("#ea580c", DEFAULT_H + 20, violin_title), showlegend=True)
        else:
            fig.update_layout(**BL("#ea580c", DEFAULT_H + 20, violin_title), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        choro_df = df_year.groupby("country")["temperature_celsius"].mean().reset_index()
        fig2 = px.choropleth(
            choro_df, locations="country", locationmode="country names",
            color="temperature_celsius",
            color_continuous_scale=["#1e3a8a","#3b82f6","#38bdf8","#fde047","#f97316","#ef4444","#7f1d1d"],
            labels={"temperature_celsius":"Avg Temp (°C)"},
        )
        fig2.update_traces(
            hovertemplate="<b>%{location}</b><br>Avg Temp: %{z:.1f}°C<extra></extra>",
            marker_line_color="#ffffff", marker_line_width=0.3,
        )
        fig2.update_geos(
            showframe=False, showcoastlines=True, coastlinecolor="#cbd5e1",
            showland=True, landcolor="#f1f5f9", showocean=True, oceancolor="#e0f2fe",
            projection_type="natural earth",
        )
        fig2.update_layout(
            paper_bgcolor=PBG, plot_bgcolor=PBG, hoverlabel=HVR,
            geo=dict(bgcolor=PBG),
            coloraxis_colorbar=dict(
                title=dict(text="°C", font=dict(color="#0f172a")),
                tickfont=dict(color="#000000"),
                bgcolor="rgba(255,255,255,0.7)", bordercolor="#cbd5e1",
            ),
            height=DEFAULT_H + 20, margin=dict(l=0, r=0, t=40, b=0),
            font=dict(color="#1e293b", size=12),
            title=dict(
                text=f"Avg Temperature by Country · {sel_year}",
                font=dict(color="#dc2626", size=13, weight="bold"), x=0.01,
            ),
        )
        highlight_country(
            fig2, sel_country,
            df_c=choro_df, col="temperature_celsius",
            label="Avg Temp (°C)", fmt=".1f",
        )
        st.plotly_chart(fig2, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        # FIX BUG-011: guard against empty monthly data
        if df_monthly.empty or len(df_monthly) == 0:
            st.info("No monthly temperature data available for this selection.")
        else:
            temps  = df_monthly["temp"].tolist()
            months = list(df_monthly["month_name"])
            deltas = [temps[0]] + [temps[i] - temps[i-1] for i in range(1, len(temps))]
            mtype  = ["absolute"] + ["relative"] * (len(temps) - 1)
            fig3   = go.Figure(go.Waterfall(
                x=months, y=deltas, measure=mtype,
                increasing=dict(marker=dict(color="#ef4444")),
                decreasing=dict(marker=dict(color="#22c55e")),
                totals=dict(marker=dict(color="#0284c7")),
                connector=dict(line=dict(color="#94a3b8", width=1.5, dash="dot")),
                text=[f"{v:+.1f}" for v in deltas], textposition="outside",
                textfont=dict(color="#0f172a", size=11, family="Inter", weight="bold"),
                hovertemplate="<b>%{x}</b><br>Change: %{y:+.2f}°C<extra></extra>",
            ))
            fig3.update_layout(**BL("#ca8a04", DEFAULT_H, f"Month-over-Month Temp Change · {scope}"))
            st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        top8 = df_year.groupby("country")["temperature_celsius"].mean().nlargest(8).reset_index()
        # FIX BUG-012: dynamic color list matching actual row count
        funnel_colors = px.colors.sequential.Reds_r[:len(top8)]
        fig4 = go.Figure(go.Funnel(
            y=top8["country"], x=top8["temperature_celsius"],
            textinfo="label+value",
            texttemplate="%{label}  <b>%{value:.1f}°C</b>",
            marker=dict(color=funnel_colors, line=dict(width=1, color="#ffffff")),
            connector=dict(line=dict(color="#cbd5e1", width=1.5)),
            hovertemplate="<b>%{y}</b><br>Avg Temp: %{x:.1f}°C<extra></extra>",
        ))
        fig4.update_layout(**BL("#ea580c", DEFAULT_H, "Top 8 Hottest Countries"))
        st.plotly_chart(fig4, use_container_width=True)

    col_l3, col_r3 = st.columns(2)

    with col_l3:
        cold10 = (df_year.groupby("country")["temperature_celsius"].mean()
                  .nsmallest(10).reset_index().sort_values("temperature_celsius"))
        # FIX BUG-008: axis padding + smart text position for negative values
        x_min = cold10["temperature_celsius"].min()
        x_max = cold10["temperature_celsius"].max()
        x_pad = abs(x_max - x_min) * 0.15 + 1
        fig5 = go.Figure()
        for _, row in cold10.iterrows():
            fig5.add_shape(type="line",
                x0=0, x1=row["temperature_celsius"],
                y0=row["country"], y1=row["country"],
                line=dict(color="#93c5fd", width=2))
        fig5.add_trace(go.Scatter(
            x=cold10["temperature_celsius"], y=cold10["country"],
            mode="markers+text",
            marker=dict(size=14, color="#3b82f6", line=dict(width=2, color="#ffffff")),
            text=cold10["temperature_celsius"].map(lambda v: f"{v:.1f}°C"),
            # FIX BUG-008: negative values get label on the left
            textposition=cold10["temperature_celsius"].apply(
                lambda v: "middle left" if v < 0 else "middle right"
            ).tolist(),
            textfont=dict(color="#000000", size=11, family="Inter", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Avg Temp: %{x:.1f}°C<extra></extra>",
        ))
        fig5.update_layout(**BL("#2563eb", DEFAULT_H, "Top 10 Coldest Countries"))
        fig5.update_xaxes(range=[x_min - x_pad, x_max + x_pad],
                          tickfont=dict(color="#000000"))
        st.plotly_chart(fig5, use_container_width=True)

    with col_r3:
        trange = (df_year.groupby("country")["temperature_celsius"]
                  .agg(t_max="max", t_min="min").reset_index())
        trange["range"] = trange["t_max"] - trange["t_min"]
        trange = trange.nlargest(10, "range").sort_values("range")
        fig6 = go.Figure(go.Bar(
            x=trange["range"], y=trange["country"], orientation="h",
            marker=dict(
                color=trange["range"],
                colorscale=[[0,"#c7d2fe"],[0.5,"#818cf8"],[1,"#4f46e5"]],
                showscale=False,
            ),
            text=trange["range"].map(lambda v: f"{v:.1f}°C"),
            textposition="outside",
            textfont=dict(color="#000000", size=11, family="Inter", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Temp Range: %{x:.1f}°C<extra></extra>",
        ))
        fig6.update_layout(**BL("#7c3aed", DEFAULT_H, "Countries with Widest Temperature Range"))
        st.plotly_chart(fig6, use_container_width=True)


# ════════════════════════════════════════════════
#  TAB 3 — PRECIPITATION & WIND
# ════════════════════════════════════════════════
with tabs[2]:
    # FIX BUG-006: meaningful precip KPI based on scope
    if sel_country == "All Countries":
        precip_kpi_val   = safe_mean(df_filtered["precip_mm"])
        precip_kpi_label = "avg monthly"
    else:
        precip_kpi_val   = df_filtered["precip_mm"].sum() if len(df_filtered) else 0
        precip_kpi_label = "cumulative"

    heavy_r = int((df_filtered["precip_mm"] > T_RAIN).sum()) if len(df_filtered) else 0
    avg_w   = safe_mean(df_filtered["wind_mps"])
    high_w  = int((df_filtered["wind_mps"] > T_WIND).sum()) if len(df_filtered) else 0
    p_mean  = df_filtered["precip_mm"].mean() if len(df_filtered) else 1
    cv      = df_filtered["precip_mm"].std() / max(p_mean, 1e-9) if len(df_filtered) else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi("🌧 Precipitation", f"{precip_kpi_val:.1f}mm", precip_kpi_label, "kpi-blue"),   unsafe_allow_html=True)
    with c2: st.markdown(kpi("⛈ Heavy Rain",     str(heavy_r),    f">{T_RAIN}mm",  "kpi-cyan"),   unsafe_allow_html=True)
    with c3: st.markdown(kpi("💨 Avg Wind",       f"{avg_w:.2f}m/s","mean speed",   "kpi-teal"),   unsafe_allow_html=True)
    with c4: st.markdown(kpi("🌪 High Wind",      str(high_w),     ">60 km/h",      "kpi-purple"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("📉 Variability CV", f"{cv:.2f}",     "rain CV index", "kpi-sky"),    unsafe_allow_html=True)

    st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["humidity"] / 10,
            mode="lines", fill="tozeroy", name="Humidity/10",
            line=dict(color="#0d9488", width=1.5), fillcolor="rgba(13,148,136,0.15)",
            hovertemplate="<b>%{x}</b><br>Humidity: %{customdata:.0f}%<extra></extra>",
            customdata=df_monthly["humidity"],
        ))
        fig.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["precip"],
            mode="lines+markers", fill="tonexty", name="Precipitation",
            line=dict(color="#2563eb", width=2.5), fillcolor="rgba(37,99,235,0.25)",
            marker=dict(size=8, color="#2563eb", line=dict(width=1.5, color="#ffffff")),
            hovertemplate="<b>%{x}</b><br>Precip: %{y:.3f}mm<extra></extra>",
        ))
        fig.update_layout(**BL("#2563eb", DEFAULT_H, f"Monthly Precipitation & Humidity · {scope}"))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # (BUG-015 fix: dead ensure_full_months call removed — wind_vals computed directly below)
        wind_vals = list(
            df_monthly.set_index("month_name")["wind"]
            .reindex(MONTH_ORDER, fill_value=0)
        )
        fig2 = go.Figure(go.Scatterpolar(
            r=wind_vals + [wind_vals[0]],
            theta=MONTH_ORDER + [MONTH_ORDER[0]],
            fill="toself", fillcolor="rgba(13,148,136,0.20)",
            line=dict(color="#0d9488", width=2.5),
            marker=dict(size=9, color="#0d9488", line=dict(width=1.5, color="#ffffff")),
            hovertemplate="<b>%{theta}</b><br>Wind: %{r:.2f}m/s<extra></extra>",
        ))
        fig2.update_layout(
            paper_bgcolor=PBG, plot_bgcolor=PBG, hoverlabel=HVR,
            polar=dict(bgcolor="rgba(0,0,0,0.02)",
                       radialaxis=dict(visible=True, gridcolor=GRD,
                                       tickcolor="#000000", color="#000000"),
                       angularaxis=dict(gridcolor=GRD, linecolor=AXC, color="#000000")),
            legend=dict(bgcolor="rgba(255,255,255,0.7)", bordercolor="rgba(0,0,0,0.1)",
                        borderwidth=1, font=dict(color="#1e293b")),
            font=dict(color="#000000", size=12), height=DEFAULT_H,
            margin=dict(l=44, r=44, t=46, b=44),
            title=dict(text="Monthly Wind Speed Polar Chart (m/s)",
                       font=dict(color="#0d9488", size=13, weight="bold"), x=0.01),
        )
        st.plotly_chart(fig2, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        tp = (df_year.groupby("country")["precip_mm"].sum()
              .nlargest(10).reset_index().sort_values("precip_mm"))
        fig3 = go.Figure(go.Bar(
            x=tp["precip_mm"], y=tp["country"], orientation="h",
            text=tp["precip_mm"].map(lambda v: f"{v:.0f}mm"),
            textposition="outside",
            textfont=dict(color="#0f172a", size=11, family="Inter", weight="bold"),
            marker=dict(
                color=tp["precip_mm"],
                colorscale=[[0,"#e0f2fe"],[0.4,"#7dd3fc"],[0.7,"#0ea5e9"],[1,"#0284c7"]],
                showscale=False, line=dict(width=0.5, color="#0284c7"),
            ),
            hovertemplate="<b>%{y}</b><br>Total Precip: %{x:.0f}mm<extra></extra>",
        ))
        fig3.update_layout(**BL("#0284c7", DEFAULT_H + 20, "Top 10 Countries by Total Precipitation"))
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=df_monthly["month_name"], y=df_monthly["precip"],
            name="Precip (mm)", marker_color="#3b82f6", opacity=0.9,
            hovertemplate="<b>%{x}</b><br>Precip: %{y:.3f}mm<extra></extra>",
        ))
        fig4.add_trace(go.Bar(
            x=df_monthly["month_name"], y=df_monthly["wind"],
            name="Wind (m/s)", marker_color="#14b8a6", opacity=0.9,
            hovertemplate="<b>%{x}</b><br>Wind: %{y:.2f}m/s<extra></extra>",
        ))
        fig4.update_layout(
            **BL("#0d9488", DEFAULT_H + 20, f"Monthly Precipitation & Wind Speed · {scope}"),
            barmode="group",
        )
        st.plotly_chart(fig4, use_container_width=True)

    precip_choro = df_year.groupby("country")["precip_mm"].mean().reset_index()
    fig6 = make_choropleth(
        precip_choro, "precip_mm",
        ["#fefce8","#86efac","#22c55e","#15803d","#052e16"],
        "Global Avg Precipitation Map", "#16a34a", "Avg Precip (mm)",
        sel_year, sel_country, fmt=".2f",
    )
    st.plotly_chart(fig6, use_container_width=True)


# ════════════════════════════════════════════════
#  TAB 4 — EXTREME EVENTS
# ════════════════════════════════════════════════
with tabs[3]:
    if len(df_filtered):
        dfe           = df_filtered.copy()
        dfe["heat"]   = (dfe["temperature_celsius"] > T_HEAT).astype(int)
        dfe["rain"]   = (dfe["precip_mm"]           > T_RAIN).astype(int)
        dfe["wind_e"] = (dfe["wind_mps"]             > T_WIND).astype(int)
        h_e   = int(dfe["heat"].sum())
        r_e   = int(dfe["rain"].sum())
        w_e   = int(dfe["wind_e"].sum())
        tot_e = h_e + r_e + w_e

        # FIX BUG-005: derive rs from the unified compute_risk_scores() result
        risk_filt = df_year_risk[
            df_year_risk["country"] == sel_country
        ] if sel_country != "All Countries" else df_year_risk
        rs = float(safe_mean(risk_filt["Risk"]))
    else:
        h_e = r_e = w_e = tot_e = 0
        rs  = 0.0
        dfe = df_filtered.copy()
        dfe["heat"] = dfe["rain"] = dfe["wind_e"] = 0

    rcat  = "🟢 Low" if rs < 20 else ("🟡 Medium" if rs < 50 else "🔴 High")

    dfy_e = df_year.copy()
    dfy_e["evts"] = (
        (dfy_e["temperature_celsius"] > T_HEAT).astype(int) +
        (dfy_e["precip_mm"]           > T_RAIN).astype(int) +
        (dfy_e["wind_mps"]             > T_WIND).astype(int)
    )
    risk_c = safe_idxmax(dfy_e.groupby("country")["evts"].sum())

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi("🚨 Total Events",  str(tot_e), "all types",            "kpi-red"),    unsafe_allow_html=True)
    with c2: st.markdown(kpi("🔥 Heatwaves",     str(h_e),   f">{T_HEAT}°C",         "kpi-orange"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("⛈ Heavy Rain",     str(r_e),   f">{T_RAIN}mm",         "kpi-blue"),   unsafe_allow_html=True)
    with c4: st.markdown(kpi("🌪 High Wind",      str(w_e),   f">{T_WIND:.0f}m/s",    "kpi-purple"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("⚠️ Highest Risk",  truncate_label(risk_c), rcat,        "kpi-yellow"), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=rs,
            delta=dict(reference=50, valueformat=".1f",
                       increasing=dict(color="#dc2626"),
                       decreasing=dict(color="#16a34a")),
            title=dict(text=f"Risk Score  ·  {rcat}",
                       font=dict(color="#0f172a", size=14)),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor="#000000", tickwidth=1),
                bar=dict(color="#dc2626", thickness=0.25),
                bgcolor="rgba(0,0,0,0.05)", bordercolor="rgba(0,0,0,0.1)",
                steps=[
                    dict(range=[0,  20], color="rgba(34,197,94,0.3)"),
                    dict(range=[20, 50], color="rgba(234,179,8,0.3)"),
                    dict(range=[50,100], color="rgba(239,68,68,0.3)"),
                ],
                threshold=dict(line=dict(color="#0f172a", width=3), thickness=0.80, value=rs),
            ),
            number=dict(font=dict(color="#0f172a", size=46), suffix="/100"),
        ))
        fig.update_layout(paper_bgcolor=PBG, plot_bgcolor=PBG, hoverlabel=HVR,
                          font=dict(color="#000000"), height=DEFAULT_H - 20,
                          margin=dict(l=30, r=30, t=52, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        top10_ext = (
            dfy_e.groupby("country")["evts"].sum()
            .nlargest(10).reset_index().sort_values("evts")
        )
        bar_clrs = [
            "#22c55e" if v < 3 else "#eab308" if v < 6 else "#ef4444"
            for v in top10_ext["evts"]
        ]
        fig2 = go.Figure(go.Bar(
            x=top10_ext["evts"], y=top10_ext["country"], orientation="h",
            marker=dict(color=bar_clrs, line=dict(width=0)),
            text=top10_ext["evts"].map(str), textposition="outside",
            textfont=dict(color="#0f172a", size=11, family="Inter", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Total Events: %{x}<extra></extra>",
        ))
        fig2.update_layout(**BL("#ea580c", DEFAULT_H - 20, "Top 10 Countries by Extreme Events"))
        fig2.update_yaxes(autorange="reversed", gridcolor=GRD, linecolor=AXC, zerolinecolor=AXC)
        st.plotly_chart(fig2, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    monthly_e = (
        dfe.groupby(["month","month_name"], observed=True)
        .agg(Heatwave=("heat","sum"), HeavyRain=("rain","sum"), HighWind=("wind_e","sum"))
        .reset_index().sort_values("month")
    )

    # FIX BUG-007: guard empty extreme events DataFrame
    if monthly_e.empty:
        with col_l2:
            st.info(f"ℹ️ No extreme events recorded for **{scope}** in **{sel_year}**.")
        with col_r2:
            st.info("Adjust the country or year to see extreme event trends.")
    else:
        with col_l2:
            heat_mat = monthly_e[["Heatwave","HeavyRain","HighWind"]].T
            heat_mat.columns = list(monthly_e["month_name"])
            fig3 = px.imshow(
                heat_mat,
                color_continuous_scale=["#f8fafc","#fecaca","#f87171","#dc2626","#991b1b"],
                text_auto=True, aspect="auto",
            )
            fig3.update_traces(
                hovertemplate="<b>%{y}</b> · %{x}<br>Count: %{z}<extra></extra>",
            )
            fig3.update_layout(**BL("#dc2626", DEFAULT_H - 60, f"Extreme Events Count (Type × Month) · {scope}"))
            st.plotly_chart(fig3, use_container_width=True)

        with col_r2:
            fig4 = go.Figure()
            for name, col_n, clr, sym in [
                ("🔥 Heatwave",  "Heatwave",  "#ef4444", "circle"),
                ("⛈ Heavy Rain", "HeavyRain", "#3b82f6", "diamond"),
                ("🌪 High Wind",  "HighWind",  "#a855f7", "triangle-up"),
            ]:
                fig4.add_trace(go.Scatter(
                    x=monthly_e["month_name"], y=monthly_e[col_n],
                    mode="lines+markers", name=name,
                    line=dict(color=clr, width=2.5),
                    marker=dict(size=8, symbol=sym, color=clr,
                                line=dict(width=1.5, color="#ffffff")),
                    hovertemplate=f"<b>%{{x}}</b><br>{name}: %{{y}}<extra></extra>",
                ))
            fig4.update_layout(**BL("#ea580c", DEFAULT_H - 60, f"Monthly Extreme Event Timeline · {scope}"))
            st.plotly_chart(fig4, use_container_width=True)


# ════════════════════════════════════════════════
#  HELPER — Country comparison chart factory
# ════════════════════════════════════════════════
def _comparison_line(dA, dB, cA, cB, metric, y_label, title, accent, **extra_kw):
    mA = dA.groupby("month")[metric].mean().reset_index()
    mB = dB.groupby("month")[metric].mean().reset_index()
    mA["mn"] = mA["month"].map(MMAP)
    mB["mn"] = mB["month"].map(MMAP)
    fig = go.Figure()
    for d, c, clr in [(mA, cA, "#ef4444"), (mB, cB, "#3b82f6")]:
        fig.add_trace(go.Scatter(
            x=d["mn"], y=d[metric], mode="lines+markers", name=c,
            line=dict(color=clr, width=2.5),
            marker=dict(size=7, color=clr, line=dict(width=1, color="#ffffff")),
            hovertemplate=f"<b>{c}</b> · %{{x}}<br>{y_label}: %{{y:.2f}}<extra></extra>",
        ))
    fig.update_layout(**BL(accent, DEFAULT_H, title), **extra_kw)
    return fig

def _comparison_bar(dA, dB, cA, cB, metric, y_label, title, accent, hline=None):
    mA = dA.groupby("month")[metric].mean().reset_index()
    mB = dB.groupby("month")[metric].mean().reset_index()
    mA["mn"] = mA["month"].map(MMAP)
    mB["mn"] = mB["month"].map(MMAP)
    fig = go.Figure()
    for d, c, clr in [(mA, cA, "#ef4444"), (mB, cB, "#3b82f6")]:
        fig.add_trace(go.Bar(
            x=d["mn"], y=d[metric], name=c, marker_color=clr, opacity=0.85,
            hovertemplate=f"<b>{c}</b> · %{{x}}<br>{y_label}: %{{y:.2f}}<extra></extra>",
        ))
    fig.update_layout(**BL(accent, DEFAULT_H, title), barmode="group")
    if hline:
        fig.add_hline(y=hline["y"], line_dash="dash", line_color="#dc2626",
                      annotation_text=hline["label"], annotation_font_color="#dc2626",
                      annotation_position="top right")
    return fig


# ════════════════════════════════════════════════
#  TAB 5 — REGIONAL COMPARISON
# ════════════════════════════════════════════════
with tabs[4]:
    clist = sorted(df_full["country"].unique().tolist())
    ca_col, cb_col = st.columns(2)
    with ca_col:
        st.markdown("**🔴 Country A**")
        cA = st.selectbox("", clist,
                          index=clist.index("India") if "India" in clist else 0,
                          key="cA", label_visibility="collapsed")
    with cb_col:
        st.markdown("**🔵 Country B**")
        cB = st.selectbox("", clist,
                          index=clist.index("China") if "China" in clist else 1,
                          key="cB", label_visibility="collapsed")

    dA = df_year[df_year["country"] == cA]
    dB = df_year[df_year["country"] == cB]

    # FIX BUG-013: guard empty comparison data
    if dA.empty or dB.empty:
        missing = [c for c, d in [(cA, dA), (cB, dB)] if d.empty]
        st.warning(f"⚠️ No data available for **{', '.join(missing)}** in **{sel_year}**. Try a different year.")
    else:
        atA, atB = safe_mean(dA["temperature_celsius"]), safe_mean(dB["temperature_celsius"])
        apA, apB = safe_mean(dA["precip_mm"]),           safe_mean(dB["precip_mm"])
        awA, awB = safe_mean(dA["wind_mps"]),             safe_mean(dB["wind_mps"])

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown(kpi(f"🌡 {truncate_label(cA, 10)}", f"{atA:.1f}°C","avg temp","kpi-red"),    unsafe_allow_html=True)
        with c2: st.markdown(kpi(f"🌡 {truncate_label(cB, 10)}", f"{atB:.1f}°C","avg temp","kpi-sky"),    unsafe_allow_html=True)
        with c3: st.markdown(kpi("🔺 Temp Diff",    f"{atA-atB:+.1f}°C","A−B","kpi-orange"),             unsafe_allow_html=True)
        with c4: st.markdown(kpi("🌧 Rain Diff",    f"{apA-apB:+.2f}mm","avg","kpi-cyan"),               unsafe_allow_html=True)
        with c5: st.markdown(kpi("💨 Wind Diff",    f"{awA-awB:+.2f}m/s","avg","kpi-teal"),              unsafe_allow_html=True)

        st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)

        col_l, col_r = st.columns(2)
        with col_l:
            metrics = ["temperature_celsius","precip_mm","wind_mps","humidity","uv_index","air_quality_PM2.5"]
            labels  = ["Temp","Precip","Wind","Humidity","UV","PM2.5"]
            vA2 = [safe_mean(dA[m]) for m in metrics]
            vB2 = [safe_mean(dB[m]) for m in metrics]
            mx  = [max(a, b, 0.001) for a, b in zip(vA2, vB2)]
            nA  = [v / m * 100 for v, m in zip(vA2, mx)]
            nB  = [v / m * 100 for v, m in zip(vB2, mx)]
            fig_r = go.Figure()
            for n, name, clr, fc in [(nA, cA, "#ef4444","rgba(239,68,68,0.25)"),
                                      (nB, cB, "#3b82f6","rgba(59,130,246,0.25)")]:
                fig_r.add_trace(go.Scatterpolar(
                    r=n + [n[0]], theta=labels + [labels[0]],
                    fill="toself", name=name, line_color=clr, fillcolor=fc,
                    hovertemplate="<b>%{theta}</b>: %{r:.1f}<extra></extra>",
                ))
            fig_r.update_layout(
                paper_bgcolor=PBG, plot_bgcolor=PBG, hoverlabel=HVR,
                polar=dict(bgcolor="rgba(0,0,0,0.02)",
                           radialaxis=dict(visible=True, range=[0,100], gridcolor=GRD,
                                           tickcolor="#000000", color="#000000"),
                           angularaxis=dict(gridcolor=GRD, linecolor=AXC, color="#000000")),
                legend=dict(bgcolor="rgba(255,255,255,0.7)", bordercolor="rgba(0,0,0,0.1)",
                            borderwidth=1, font=dict(color="#1e293b")),
                font=dict(color="#000000", size=12), height=DEFAULT_H + 20,
                margin=dict(l=44, r=44, t=46, b=44),
                title=dict(text=f"Climate Radar — {cA} vs {cB}",
                           font=dict(color="#7c3aed", size=13, weight="bold"), x=0.01),
            )
            st.plotly_chart(fig_r, use_container_width=True)

        with col_r:
            mA = dA.groupby("month")["temperature_celsius"].mean().reset_index()
            mB = dB.groupby("month")["temperature_celsius"].mean().reset_index()
            mg = mA.merge(mB, on="month", suffixes=("_A","_B"))
            mg["mn"] = mg["month"].map(MMAP)
            fig_d = go.Figure()
            for _, row in mg.iterrows():
                fig_d.add_shape(type="line",
                    x0=row["temperature_celsius_A"], x1=row["temperature_celsius_B"],
                    y0=row["mn"], y1=row["mn"],
                    line=dict(color="#cbd5e1", width=2.5))
            for data_col, name, clr in [
                ("temperature_celsius_A", cA, "#ef4444"),
                ("temperature_celsius_B", cB, "#3b82f6"),
            ]:
                fig_d.add_trace(go.Scatter(
                    x=mg[data_col], y=mg["mn"], mode="markers", name=name,
                    marker=dict(size=14, color=clr, line=dict(width=1.5, color="#ffffff")),
                    hovertemplate=f"<b>{name}</b> · %{{y}}<br>Temp: %{{x:.1f}}°C<extra></extra>",
                ))
            fig_d.update_layout(**BL("#db2777", DEFAULT_H + 20, f"Monthly Temp Dumbbell — {cA} vs {cB}"))
            st.plotly_chart(fig_d, use_container_width=True)

        col_r3a, col_r3b = st.columns(2)
        with col_r3a:
            st.plotly_chart(
                _comparison_line(dA, dB, cA, cB, "wind_mps", "m/s",
                                 f"Monthly Wind Speed — {cA} vs {cB}", "#0d9488"),
                use_container_width=True,
            )
        with col_r3b:
            st.plotly_chart(
                _comparison_line(dA, dB, cA, cB, "humidity", "%",
                                 f"Monthly Humidity — {cA} vs {cB}", "#0284c7"),
                use_container_width=True,
            )

        col_r4a, col_r4b = st.columns(2)
        with col_r4a:
            st.plotly_chart(
                _comparison_bar(dA, dB, cA, cB, "uv_index", "UV",
                                f"Monthly UV Index — {cA} vs {cB}", "#f97316",
                                hline={"y": 8, "label": "High UV (8)"}),
                use_container_width=True,
            )
        with col_r4b:
            st.plotly_chart(
                _comparison_line(dA, dB, cA, cB, "air_quality_PM2.5", "µg/m³",
                                 f"Monthly PM2.5 — {cA} vs {cB}", "#8b5cf6"),
                use_container_width=True,
            )

        col_r5a, col_r5b = st.columns(2)
        with col_r5a:
            avgA_cl = safe_mean(dA["cloud"])
            avgB_cl = safe_mean(dB["cloud"])
            fig10 = make_subplots(rows=1, cols=2,
                                  specs=[[{"type":"domain"},{"type":"domain"}]],
                                  subplot_titles=[truncate_label(cA, 15), truncate_label(cB, 15)])
            for i, (val, name, clr) in enumerate([
                (avgA_cl, cA, "#3b82f6"), (avgB_cl, cB, "#ef4444")
            ], 1):
                fig10.add_trace(go.Pie(
                    values=[val, 100 - val], labels=["Cloud Cover","Clear Sky"],
                    marker_colors=[clr,"#f1f5f9"], hole=0.65, showlegend=False, textinfo="none",
                    hovertemplate=f"<b>{name}</b><br>%{{label}}: %{{value:.1f}}%<extra></extra>",
                ), row=1, col=i)
            fig10.add_annotation(text=f"{avgA_cl:.0f}%", x=0.18, y=0.5,
                font=dict(size=20, color="#3b82f6", family="Inter"), showarrow=False)
            fig10.add_annotation(text=f"{avgB_cl:.0f}%", x=0.82, y=0.5,
                font=dict(size=20, color="#ef4444", family="Inter"), showarrow=False)
            fig10.update_layout(paper_bgcolor=PBG, plot_bgcolor=PBG, hoverlabel=HVR,
                font=dict(color="#000000", size=12), height=DEFAULT_H,
                margin=dict(l=20, r=20, t=60, b=20),
                title=dict(text=f"Avg Cloud Cover — {cA} vs {cB}",
                           font=dict(color="#0284c7", size=13, weight="bold"), x=0.01))
            st.plotly_chart(fig10, use_container_width=True)

        with col_r5b:
            st.plotly_chart(
                _comparison_bar(dA, dB, cA, cB, "precip_mm", "mm",
                                f"Monthly Precipitation — {cA} vs {cB}", "#0284c7"),
                use_container_width=True,
            )

        metrics_cmp = ["temperature_celsius","precip_mm","wind_mps","humidity","uv_index","air_quality_PM2.5"]
        labels_cmp  = ["Avg Temp (°C)","Avg Precip (mm)","Avg Wind (m/s)","Humidity (%)","UV Index","PM2.5 (µg/m³)"]
        vals_A      = [round(safe_mean(dA[m]), 2) for m in metrics_cmp]
        vals_B      = [round(safe_mean(dB[m]), 2) for m in metrics_cmp]
        fig_last = go.Figure()
        for name, vals, clr in [(cA, vals_A, "#ef4444"), (cB, vals_B, "#3b82f6")]:
            fig_last.add_trace(go.Bar(
                name=name, x=labels_cmp, y=vals, marker_color=clr, opacity=0.95,
                text=[str(v) for v in vals], textposition="outside",
                textfont=dict(color="#0f172a", size=11, family="Inter", weight="bold"),
                hovertemplate=f"<b>{name}</b><br>%{{x}}: %{{y}}<extra></extra>",
            ))
        fig_last.update_layout(
            **BL("#0d9488", DEFAULT_H + 20, f"All Climate Metrics — {cA} vs {cB} (Side-by-Side)"),
            barmode="group",
        )
        st.plotly_chart(fig_last, use_container_width=True)


# ════════════════════════════════════════════════
#  TAB 6 — HUMIDITY & CLOUD
# ════════════════════════════════════════════════
with tabs[5]:
    avg_h = safe_mean(df_filtered["humidity"])
    max_h = df_filtered["humidity"].max() if len(df_filtered) else 0
    avg_c = safe_mean(df_filtered["cloud"])
    ccd   = df_year.groupby("country")["cloud"].mean()
    cld_c = safe_idxmax(ccd)
    crv   = (df_filtered["humidity"].corr(df_filtered["temperature_celsius"])
             if len(df_filtered) > 1 else 0)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi("💧 Avg Humidity", f"{avg_h:.1f}%", scope,                  "kpi-blue"),   unsafe_allow_html=True)
    with c2: st.markdown(kpi("🌊 Max Humidity", f"{max_h:.1f}%", "highest",              "kpi-cyan"),   unsafe_allow_html=True)
    with c3: st.markdown(kpi("☁️ Avg Cloud",   f"{avg_c:.1f}%", "coverage",             "kpi-teal"),   unsafe_allow_html=True)
    with c4: st.markdown(kpi("🌫 Cloudiest",   truncate_label(cld_c), f"{ccd.max():.1f}%","kpi-purple"),unsafe_allow_html=True)
    with c5: st.markdown(kpi("🔗 Correlation", f"{crv:.2f}",    "Humidity vs Temp",      "kpi-orange"), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["humidity"],
            mode="lines+markers", fill="tozeroy",
            line=dict(color="#0284c7", width=3, shape="spline"),
            fillcolor="rgba(2,132,199,0.18)",
            marker=dict(size=8, color="#0284c7", line=dict(width=2, color="#ffffff")),
            hovertemplate="<b>%{x}</b><br>Humidity: %{y:.1f}%<extra></extra>",
            name="Humidity",
        ))
        avg_h_m = df_monthly["humidity"].mean()
        fig.add_hline(y=avg_h_m, line_dash="dot", line_color="#f59e0b", line_width=2,
                      annotation_text=f"Avg {avg_h_m:.1f}%",
                      annotation_font=dict(color="#b45309", size=11))
        fig.update_layout(**BL("#0284c7", DEFAULT_H, f"Monthly Humidity Trend · {scope}"))
        fig.update_yaxes(range=[0, 105])
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        cloud_full = (
            df_monthly.set_index("month_name")["cloud"]
            .reindex(MONTH_ORDER, fill_value=0)
        )
        fig2 = go.Figure(go.Barpolar(
            r=list(cloud_full), theta=MONTH_ORDER,
            width=[1] * 12,
            marker=dict(
                color=list(cloud_full),
                colorscale=[[0,"#e0f2fe"],[0.4,"#38bdf8"],[0.7,"#0284c7"],[1,"#1e3a8a"]],
                showscale=True,
                colorbar=dict(title=dict(text="%", font=dict(color="#000000")),
                              tickfont=dict(color="#000000"), thickness=12),
            ),
            hovertemplate="<b>%{theta}</b><br>Cloud Cover: %{r:.1f}%<extra></extra>",
        ))
        fig2.update_layout(
            paper_bgcolor=PBG, plot_bgcolor=PBG, hoverlabel=HVR,
            polar=dict(
                bgcolor="rgba(0,0,0,0.02)",
                radialaxis=dict(range=[0,100], tickfont=dict(color="#000000", size=9),
                                gridcolor=GRD, tickcolor="#000000"),
                angularaxis=dict(tickfont=dict(color="#000000", size=10),
                                 gridcolor=GRD, linecolor=AXC),
            ),
            font=dict(color="#000000", size=12), height=DEFAULT_H,
            margin=dict(l=44, r=60, t=46, b=44),
            title=dict(text=f"Monthly Cloud Cover — Polar · {scope}",
                       font=dict(color="#0d9488", size=13, weight="bold"), x=0.01),
        )
        st.plotly_chart(fig2, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        th = (df_year.groupby("country")["humidity"].mean()
              .nlargest(10).reset_index().sort_values("humidity"))
        fig3 = go.Figure()
        for _, row in th.iterrows():
            fig3.add_shape(type="line",
                x0=0, x1=row["humidity"], y0=row["country"], y1=row["country"],
                line=dict(color="#93c5fd", width=2))
        fig3.add_trace(go.Scatter(
            x=th["humidity"], y=th["country"], mode="markers+text",
            text=th["humidity"].map(lambda v: f"{v:.0f}%"),
            textposition="middle right", textfont=dict(color="#000000", size=10),
            marker=dict(size=13, color="#0284c7", line=dict(width=2, color="#ffffff")),
            name="Humidity %",
            hovertemplate="<b>%{y}</b><br>Humidity: %{x:.1f}%<extra></extra>",
        ))
        fig3.update_layout(**BL("#0284c7", DEFAULT_H, f"Top 10 Most Humid Countries · {sel_year}"))
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        top10_h = df_year.groupby("country")["humidity"].mean().nlargest(10).index
        hc_bar  = (df_year[df_year["country"].isin(top10_h)]
                   .groupby("country").agg(humidity=("humidity","mean"), cloud=("cloud","mean"))
                   .reset_index().sort_values("humidity", ascending=False))
        fig4 = go.Figure()
        for metric, name, clr in [("humidity","Humidity (%)","#0284c7"),
                                   ("cloud","Cloud Cover (%)","#7c3aed")]:
            fig4.add_trace(go.Bar(
                name=name, x=hc_bar["country"], y=hc_bar[metric],
                marker_color=clr, opacity=0.88,
                text=hc_bar[metric].map(lambda v: f"{v:.0f}%"),
                textposition="outside", textfont=dict(color="#000000", size=9),
                hovertemplate=f"<b>%{{x}}</b><br>{name}: %{{y:.1f}}%<extra></extra>",
            ))
        fig4.update_layout(
            **BL("#0284c7", DEFAULT_H,
                 f"Humidity vs Cloud Cover — Top 10 Humid Countries · {sel_year}"),
            barmode="group",
        )
        fig4.update_xaxes(tickangle=-30, tickfont=dict(color="#000000", size=9))
        st.plotly_chart(fig4, use_container_width=True)

    col_l3, col_r3 = st.columns(2)

    with col_l3:
        tc2 = (df_year.groupby("country")["cloud"].mean()
               .nlargest(10).reset_index().sort_values("cloud"))
        fig_cl = go.Figure()
        for _, row in tc2.iterrows():
            fig_cl.add_shape(type="line",
                x0=0, x1=row["cloud"], y0=row["country"], y1=row["country"],
                line=dict(color="#c4b5fd", width=2))
        fig_cl.add_trace(go.Scatter(
            x=tc2["cloud"], y=tc2["country"], mode="markers+text",
            text=tc2["cloud"].map(lambda v: f"{v:.1f}%"),
            textposition="middle right",
            textfont=dict(color="#000000", size=10, family="Inter", weight="bold"),
            marker=dict(size=14, color="#7c3aed", line=dict(width=2, color="#ffffff")),
            name="Cloud Cover %",
            hovertemplate="<b>%{y}</b><br>Cloud Cover: %{x:.1f}%<extra></extra>",
        ))
        fig_cl.update_layout(**BL("#7c3aed", DEFAULT_H, f"Top 10 Cloudiest Countries · {sel_year}"))
        st.plotly_chart(fig_cl, use_container_width=True)

    with col_r3:
        fig_dual = go.Figure()
        fig_dual.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["humidity"],
            mode="lines+markers", fill="tozeroy", name="Humidity (%)",
            line=dict(color="#0284c7", width=2.5, shape="spline"),
            fillcolor="rgba(2,132,199,0.15)", marker=dict(size=7, color="#0284c7"),
            hovertemplate="<b>%{x}</b><br>Humidity: %{y:.1f}%<extra></extra>",
        ))
        fig_dual.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["cloud"],
            mode="lines+markers", fill="tonexty", name="Cloud Cover (%)",
            line=dict(color="#7c3aed", width=2.5, shape="spline"),
            fillcolor="rgba(124,58,237,0.12)", marker=dict(size=7, color="#7c3aed"),
            hovertemplate="<b>%{x}</b><br>Cloud: %{y:.1f}%<extra></extra>",
        ))
        fig_dual.update_layout(**BL("#0284c7", DEFAULT_H, f"Humidity & Cloud Cover Overlay · {scope}"))
        st.plotly_chart(fig_dual, use_container_width=True)


# ════════════════════════════════════════════════
#  TAB 7 — UV & AIR QUALITY
# ════════════════════════════════════════════════
with tabs[6]:
    avg_uv = safe_mean(df_filtered["uv_index"])
    max_uv = df_filtered["uv_index"].max() if len(df_filtered) else 0
    avg_p2 = safe_mean(df_filtered["air_quality_PM2.5"])
    avg_p1 = safe_mean(df_filtered["air_quality_PM10"])
    p_c    = df_year.groupby("country")["air_quality_PM2.5"].mean()
    mp_c   = safe_idxmax(p_c)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi("☀️ Avg UV",      f"{avg_uv:.1f}", scope,                     "kpi-orange"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("🔥 Max UV",      f"{max_uv:.1f}", "highest",                  "kpi-red"),    unsafe_allow_html=True)
    with c3: st.markdown(kpi("🌫️ Avg PM2.5",  f"{avg_p2:.1f}", "µg/m³",                   "kpi-purple"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("🏭 Avg PM10",   f"{avg_p1:.1f}", "µg/m³",                   "kpi-pink"),   unsafe_allow_html=True)
    with c5: st.markdown(kpi("⚠️ Poorest Air",truncate_label(mp_c), f"{safe_max(p_c):.1f} PM2.5","kpi-yellow"),unsafe_allow_html=True)

    st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)
    bx = "alert-box" if avg_p2 > WHO_PM25 else "ok-box"
    bm = (f"🟡 PM2.5 Alert: {scope} averages {avg_p2:.1f} µg/m³ — above WHO limit ({WHO_PM25} µg/m³)."
          if avg_p2 > WHO_PM25
          else f"✅ {scope} PM2.5 is below the WHO limit ({WHO_PM25} µg/m³).")
    st.markdown(f"<div class='{bx}'>{bm}</div>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        fig = make_subplots(rows=1, cols=2,
                            specs=[[{"type":"scatter"},{"type":"indicator"}]],
                            column_widths=[0.6, 0.4])
        fig.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["uv"],
            mode="lines+markers", line=dict(color="#f97316", width=2.5),
            marker=dict(size=6, color="#f97316"),
            hovertemplate="<b>%{x}</b><br>UV: %{y:.1f}<extra></extra>",
        ), row=1, col=1)
        # FIX BUG-014: only add avg hline when there are at least 2 data points
        if len(df_monthly) >= 2:
            fig.add_trace(go.Scatter(
                x=[df_monthly["month_name"].iloc[0], df_monthly["month_name"].iloc[-1]],
                y=[avg_uv, avg_uv],
                mode="lines", line=dict(color="#ea580c", width=1.5, dash="dot"),
                name="Avg UV", hoverinfo="skip",
            ), row=1, col=1)
        fig.add_trace(go.Indicator(
            mode="gauge+number", value=avg_uv,
            number=dict(font=dict(size=36, color="#0f172a")),
            gauge=dict(
                axis=dict(range=[0, 12], tickcolor="#000000"),
                bar=dict(color="#f97316"),
                steps=[
                    dict(range=[0, 3],  color="rgba(34,197,94,0.3)"),
                    dict(range=[3, 8],  color="rgba(234,179,8,0.3)"),
                    dict(range=[8, 12], color="rgba(239,68,68,0.3)"),
                ],
            ),
        ), row=1, col=2)
        fig.update_layout(**BL("#ea580c", DEFAULT_H - 40,
                               f"Monthly UV Index Trend & Avg UV Gauge — {scope}"),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        dev       = df_monthly.copy()
        dev["diff"] = dev["pm25"] - WHO_PM25
        clrs      = ["#ef4444" if d > 0 else "#22c55e" for d in dev["diff"]]
        fig2 = go.Figure(go.Bar(
            x=dev["month_name"], y=dev["diff"],
            marker_color=clrs,
            text=dev["pm25"].map(lambda v: f"{v:.1f}"), textposition="outside",
            textfont=dict(color="#0f172a", size=11, family="Inter", weight="bold"),
            hovertemplate="<b>%{x}</b><br>PM2.5: %{text} µg/m³<extra></extra>",
        ))
        fig2.add_hline(y=0, line_width=1.5, line_color="#0f172a")
        fig2.update_layout(**BL("#7c3aed", DEFAULT_H - 40, f"Monthly PM2.5 vs WHO Target · {scope}"))
        st.plotly_chart(fig2, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        aq_monthly = (
            df_filtered
            .groupby(["month","month_name"], observed=True)
            .agg(pm25_avg=("air_quality_PM2.5","mean"),
                 pm10_avg=("air_quality_PM10", "mean"))
            .reset_index().sort_values("month")
        )
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=aq_monthly["month_name"], y=aq_monthly["pm10_avg"],
            fill="tozeroy", name="Avg PM10", line=dict(color="#d946ef", width=2),
            fillcolor="rgba(217,70,239,0.15)",
            hovertemplate="<b>%{x}</b><br>Avg PM10: %{y:.1f} µg/m³<extra></extra>",
        ))
        fig3.add_trace(go.Scatter(
            x=aq_monthly["month_name"], y=aq_monthly["pm25_avg"],
            fill="tozeroy", name="Avg PM2.5", line=dict(color="#ec4899", width=2),
            fillcolor="rgba(236,72,153,0.35)",
            hovertemplate="<b>%{x}</b><br>Avg PM2.5: %{y:.1f} µg/m³<extra></extra>",
        ))
        if not aq_monthly.empty:
            fig3.add_trace(go.Scatter(
                x=[aq_monthly["month_name"].iloc[0], aq_monthly["month_name"].iloc[-1]],
                y=[WHO_PM25, WHO_PM25],
                mode="lines", name="WHO Limit (15)",
                line=dict(color="#ef4444", width=2, dash="dashdot"),
            ))
        fig3.update_layout(**BL("#db2777", DEFAULT_H - 20, f"Monthly Avg PM2.5 & PM10 — {scope}"))
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        fig4 = make_subplots(specs=[[{"secondary_y": True}]])
        fig4.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["uv"],
            name="UV Index", mode="lines+markers",
            line=dict(color="#f97316", width=2.5), marker=dict(size=7),
            hovertemplate="<b>%{x}</b><br>UV: %{y:.1f}<extra></extra>",
        ), secondary_y=False)
        fig4.add_trace(go.Scatter(
            x=df_monthly["month_name"], y=df_monthly["pm25"],
            name="PM2.5", mode="lines+markers",
            line=dict(color="#ec4899", width=2.5), marker=dict(size=7),
            hovertemplate="<b>%{x}</b><br>PM2.5: %{y:.1f}<extra></extra>",
        ), secondary_y=True)
        fig4.update_layout(**BL("#0284c7", DEFAULT_H - 20, f"UV Index and PM2.5 Timeline · {scope}"))
        fig4.update_yaxes(title_text="UV Index", secondary_y=False, gridcolor=GRD,
                          linecolor=AXC, tickfont=dict(color="#000000"),
                          title_font=dict(color="#000000"))
        fig4.update_yaxes(title_text="PM2.5", secondary_y=True,
                          gridcolor="rgba(0,0,0,0)", linecolor=AXC,
                          tickfont=dict(color="#000000"), title_font=dict(color="#000000"))
        st.plotly_chart(fig4, use_container_width=True)

    col_l3, col_r3 = st.columns(2)

    with col_l3:
        pm_df  = (df_year.groupby("country")["air_quality_PM2.5"].mean()
                  .nlargest(15).reset_index().sort_values("air_quality_PM2.5"))
        pm_clrs = ["#22c55e" if v < 15 else "#f59e0b" if v < 35 else "#ef4444"
                   for v in pm_df["air_quality_PM2.5"]]
        fig5 = go.Figure(go.Bar(
            x=pm_df["air_quality_PM2.5"], y=pm_df["country"], orientation="h",
            marker=dict(color=pm_clrs, line=dict(width=0)),
            text=pm_df["air_quality_PM2.5"].map(lambda v: f"{v:.1f}"),
            textposition="outside",
            textfont=dict(color="#000000", size=10, family="Inter", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Avg PM2.5: %{x:.1f} µg/m³<extra></extra>",
        ))
        fig5.add_vline(x=WHO_PM25, line_dash="dash", line_color="#ef4444")
        fig5.update_layout(**BL("#dc2626", DEFAULT_H + 20,
                               f"Top 15 Most Polluted — PM2.5 (WHO: {WHO_PM25} µg/m³)"))
        st.plotly_chart(fig5, use_container_width=True)

    with col_r3:
        pm10_df  = (df_year.groupby("country")["air_quality_PM10"].mean()
                   .nlargest(15).reset_index().sort_values("air_quality_PM10"))
        pm10_clrs = ["#22c55e" if v < 45 else "#f59e0b" if v < 100 else "#ef4444"
                     for v in pm10_df["air_quality_PM10"]]
        fig6 = go.Figure(go.Bar(
            x=pm10_df["air_quality_PM10"], y=pm10_df["country"], orientation="h",
            marker=dict(color=pm10_clrs, line=dict(width=0)),
            text=pm10_df["air_quality_PM10"].map(lambda v: f"{v:.1f}"),
            textposition="outside",
            textfont=dict(color="#000000", size=10, family="Inter", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Avg PM10: %{x:.1f} µg/m³<extra></extra>",
        ))
        fig6.add_vline(x=WHO_PM10, line_dash="dash", line_color="#ef4444")
        fig6.update_layout(**BL("#db2777", DEFAULT_H + 20,
                               f"Top 15 Most Polluted — PM10 (WHO: {WHO_PM10} µg/m³)"))
        st.plotly_chart(fig6, use_container_width=True)


# ════════════════════════════════════════════════
#  TAB 8 — CLIMATE RISK INDEX
# ════════════════════════════════════════════════
with tabs[7]:
    # FIX BUG-003: pass df_full; FIX BUG-005: single unified risk formula
    df_year_risk_filt = (
        df_year_risk[df_year_risk["country"] == sel_country].copy()
        if sel_country != "All Countries"
        else df_year_risk.copy()
    )
    avg_rs = safe_mean(df_year_risk_filt["Risk"])
    r_cat  = "🟢 Low" if avg_rs < 30 else ("🟡 Medium" if avg_rs < 60 else "🔴 High")
    r_vol  = df_year_risk_filt["Risk"].std() if len(df_year_risk_filt) > 1 else 0

    if prev_avg_t is not None and len(df_prev):
        dp      = compute_risk_scores(df_full, sel_year - 1)
        dp_filt = dp[dp["country"] == sel_country] if sel_country != "All Countries" else dp
        r_tr    = avg_rs - safe_mean(dp_filt["Risk"])
    else:
        r_tr = 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi("⚡ Avg Risk",   f"{avg_rs:.1f}/100", scope,         "kpi-red"),    unsafe_allow_html=True)
    with c2: st.markdown(kpi("📊 Category",  r_cat,               "severity",    "kpi-orange"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("📉 Volatility",f"{r_vol:.1f}",      "std dev",     "kpi-purple"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("📈 Trend",     f"{r_tr:+.1f}",      f"vs {sel_year-1}","kpi-yellow"),unsafe_allow_html=True)

    st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=avg_rs,
            delta=dict(reference=50, valueformat=".1f",
                       increasing=dict(color="#dc2626"),
                       decreasing=dict(color="#16a34a")),
            title=dict(
                text=(f"<b style='font-size:17px;color:#0f172a;'>{scope}</b>"
                      f"<span style='font-size:13px;color:#64748b;'> · {sel_year}</span><br>"
                      f"<span style='font-size:11px;color:#475569;'>"
                      f"Category: {r_cat}  ·  Trend vs {sel_year-1}: {r_tr:+.1f}"
                      f"</span>"),
                font=dict(color="#0f172a", size=15),
            ),
            gauge=dict(
                axis=dict(range=[0,100], tickcolor="#000000", tickwidth=1,
                          tickfont=dict(color="#000000", size=11)),
                bar=dict(color="#dc2626", thickness=0.28),
                bgcolor="rgba(0,0,0,0.03)", bordercolor="rgba(0,0,0,0.08)",
                steps=[
                    dict(range=[0,  30], color="rgba(34,197,94,0.25)"),
                    dict(range=[30, 60], color="rgba(234,179,8,0.25)"),
                    dict(range=[60,100], color="rgba(239,68,68,0.25)"),
                ],
                threshold=dict(line=dict(color="#0f172a", width=3), thickness=0.85, value=avg_rs),
            ),
            number=dict(font=dict(color="#0f172a", size=48, family="Inter"), suffix="/100"),
        ))
        fig_gauge.update_layout(
            paper_bgcolor=PBG, plot_bgcolor=PBG, hoverlabel=HVR,
            font=dict(color="#000000"), height=DEFAULT_H + 20,
            margin=dict(l=30, r=30, t=90, b=20),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_r:
        r_m = (df_year_risk_filt
               .groupby("month_name", observed=True)["Risk"].mean()
               .reindex(MONTH_ORDER, fill_value=0)
               .reset_index())
        r_m.columns = ["month_name","Risk"]
        fig2 = go.Figure(go.Scatter(
            x=r_m["month_name"], y=r_m["Risk"],
            mode="lines+markers", line=dict(color="#ef4444", width=3, shape="spline"),
            marker=dict(size=9, color="#ef4444", line=dict(width=1.5, color="#ffffff")),
            fill="tozeroy", fillcolor="rgba(239,68,68,0.15)",
            hovertemplate="<b>%{x}</b><br>Risk: %{y:.1f}<extra></extra>",
        ))
        fig2.update_layout(**BL("#ea580c", DEFAULT_H + 20, f"Average Risk Score Timeline · {scope}"))
        fig2.update_yaxes(range=[0, max(100, r_m["Risk"].max() + 10)],
                          gridcolor=GRD, linecolor=AXC, zerolinecolor=AXC)
        st.plotly_chart(fig2, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        # FIX PERF-001: use cached aggregation
        r_ct = compute_top40_risk(df_full, sel_year)
        fig_tm = px.treemap(
            r_ct, path=["country"], values="Risk", color="Risk",
            color_continuous_scale=["#fef3c7","#f59e0b","#ef4444","#7f1d1d"],
        )
        fig_tm.update_traces(
            textfont=dict(color="#ffffff", size=12, family="Inter", weight="bold"),
            hovertemplate="<b>%{label}</b><br>Risk: %{color:.1f}<extra></extra>",
        )
        fig_tm.update_layout(**BL("#dc2626", DEFAULT_H + 20, f"Top 40 Highest Risk Countries · {sel_year}"))
        fig_tm.update_coloraxes(showscale=False)
        st.plotly_chart(fig_tm, use_container_width=True)

    with col_r2:
        t15 = (df_year_risk.groupby("country")["Risk"].mean()
               .nlargest(15).reset_index().sort_values("Risk"))
        fig_t15 = go.Figure(go.Bar(
            y=t15["country"], x=t15["Risk"], orientation="h",
            marker=dict(color=t15["Risk"], colorscale="Reds", showscale=False),
            text=t15["Risk"].map(lambda v: f"{v:.1f}"), textposition="outside",
            textfont=dict(color="#0f172a", size=11, family="Inter", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Risk: %{x:.1f}<extra></extra>",
        ))
        fig_t15.update_layout(**BL("#dc2626", DEFAULT_H + 20, f"Top 15 Countries by Risk Index · {sel_year}"))
        fig_t15.update_xaxes(gridcolor=GRD, linecolor=AXC, zerolinecolor=AXC,
                             tickfont=dict(color="#000000"))
        st.plotly_chart(fig_t15, use_container_width=True)

    risk_choro_df = df_year_risk.groupby("country")["Risk"].mean().reset_index()
    fig_map = make_choropleth(
        risk_choro_df, "Risk",
        ["#f0fdf4","#fde68a","#f97316","#dc2626","#7f1d1d"],
        "Global Climate Risk Score Map", "#dc2626", "Risk Score (/100)",
        sel_year, sel_country, fmt=".1f",
    )
    st.plotly_chart(fig_map, use_container_width=True)