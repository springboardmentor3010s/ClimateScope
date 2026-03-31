import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import numpy as np
import statsmodels.api as sm

# ==========================================================
# 💎 PREMIUM UI & GLOBAL CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="Climate Intel | Infinity Command",
    layout="wide",
    page_icon="🌍",
)

# Deep Obsidian & High-Contrast Visibility CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { background: radial-gradient(circle at 50% -20%, #1e293b 0%, #020617 80%) !important; }
    [data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid rgba(16, 185, 129, 0.2); }
    
    /* GLOBAL TEXT VISIBILITY FIX */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, li, label, .stRadio label { 
        font-family: 'Space Grotesk', sans-serif; 
        color: #FFFFFF !important; 
    }

    /* ELITE KPI CARDS WITH SPARKLINE SUPPORT */
    .metric-card {
        background: rgba(15, 23, 42, 0.8); 
        padding: 15px; border-radius: 12px;
        border: 1px solid rgba(16, 185, 129, 0.3);
        margin-bottom: 10px;
    }
    .metric-label { color: #10b981; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { color: #FFFFFF; font-size: 1.4rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }

    /* CORE INSIGHT BLOCK */
    .insight-block {
        background: rgba(16, 185, 129, 0.08); border-left: 5px solid #10b981;
        padding: 20px; border-radius: 4px; color: #FFFFFF; font-size: 0.95rem; 
        margin: 15px 0 60px 0; line-height: 1.6;
    }

    /* WIDGET LABELS */
    [data-testid="stWidgetLabel"] p { color: #10b981 !important; font-weight: 700 !important; }
    [data-testid="stMetricValue"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# 🛠️ GLOBAL HELPER FUNCTIONS
# ==========================================================
@st.cache_data
def get_grouped_risk(df):
    """Performance Cache for heavy calculation."""
    return df.groupby("country")["Risk_Score"].mean()

def kpi_sparkline(label, value, series):
    """Renders a KPI card with a tiny trend graph."""
    with st.container():
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div>', unsafe_allow_html=True)
        if not series.empty:
            fig = px.line(series, x=series.index, y=series.values, height=35)
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_visible=False, 
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template="plotly_dark")
            fig.update_traces(line_color="#10b981", line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

def kpi_basic(label, value):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

def apply_viz(fig, title, insight_text):
    """Styles and renders charts in a one-by-one layout."""
    fig.update_layout(
        title=dict(text=f"<span style='color:#10b981'>//</span> {title.upper()}", font=dict(size=18, family="JetBrains Mono", color='#FFFFFF')),
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=100, b=40), font=dict(family="Space Grotesk"),
    )
    fig.update_xaxes(showgrid=False, title_font_color="#10b981", tickfont_color="#FFFFFF")
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title_font_color="#10b981", tickfont_color="#FFFFFF")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f'<div class="insight-block"><b>PRESENTATION INSIGHT:</b> {insight_text}</div>', unsafe_allow_html=True)

# ==========================================================
# 📊 DATA ENGINE
# ==========================================================
@st.cache_data
def load_and_process_data():
    df = pd.read_csv("finalised_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])
    df['pressure_mb'] = df['pressure_mb'].clip(lower=950, upper=1050)
    
    t_min, t_max = df['temperature_celsius'].min(), df['temperature_celsius'].max()
    norm_temp = (df['temperature_celsius'] - t_min) / (t_max - t_min)
    norm_precip = df['precip_mm'] / df['precip_mm'].max() if df['precip_mm'].max() > 0 else 0
    norm_wind = df['wind_kph'] / df['wind_kph'].max() if df['wind_kph'].max() > 0 else 0
    
    df["Risk_Score"] = (norm_temp * 0.45 + norm_precip * 0.25 + norm_wind * 0.30)
    df["Extreme_Event"] = ((df["temperature_celsius"] > 40) | (df["precip_mm"] > 100) | (df["wind_kph"] > 60)).astype(int)
    return df

df = load_and_process_data()

# ==========================================================
# 🛰️ NAVIGATION & FILTERS
# ==========================================================
with st.sidebar:
    st.markdown("<h2 style='color:#10b981; font-weight:900;'>COMMAND CONTROL</h2>", unsafe_allow_html=True)
    countries_list = sorted(df["country"].unique())
    country_sel = st.multiselect("Select Countries", countries_list, placeholder="Global View")
    years_range = st.slider("Select Timeline", int(df["year"].min()), int(df["year"].max()), (int(df["year"].min()), int(df["year"].max())))
    seasons_sel = st.multiselect("Select Season", ["Winter", "Spring", "Summer", "Autumn"])
    st.divider()
    st.caption("Infinity Engine v16.1 Operational")

mask = (df["year"] >= years_range[0]) & (df["year"] <= years_range[1])
if country_sel: mask &= df["country"].isin(country_sel)
if seasons_sel:
    s_map = {"Winter":[12,1,2], "Spring":[3,4,5], "Summer":[6,7,8], "Autumn":[9,10,11]}
    m_filter = [m for s in seasons_sel for m in s_map[s]]
    mask &= df["month"].isin(m_filter)

f_df = df.loc[mask].copy().reset_index(drop=True)

# Safety checks & Global variables
if f_df.empty:
    st.warning("No data available for selected filters. Please adjust your criteria.")
    st.stop()

# FIX: Define hub_name globally for all sections to access
hub_name = get_grouped_risk(f_df).idxmax() if not f_df.empty else "N/A"

selected = option_menu(
    menu_title=None,
    options=["Climate Overview", "Temperature Analysis", "Rainfall & Wind", "Extreme Events", "Country Comparison", "Risk Index"],
    icons=["grid", "thermometer-sun", "moisture", "exclamation-diamond", "shuffle", "shield-lock"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "rgba(15, 23, 42, 0.95)", "border-radius": "0px", "padding": "0!important", "border-bottom": "2px solid #10b981"},
        "nav-link": {"font-size": "12px", "font-weight": "700", "color": "#FFFFFF"},
        "nav-link-selected": {"background-color": "#10b981", "color": "#020617"},
    }
)

# ==========================================================
# 🌍 1. CLIMATE OVERVIEW
# ==========================================================
if selected == "Climate Overview":
    st.markdown("<h1 style='color:#FFFFFF; font-weight:900;'>🌍 EXECUTIVE DASHBOARD</h1>", unsafe_allow_html=True)
    
    k_cols = st.columns(6)
    k_metrics = [
        ("Mean Temp", f"{f_df['temperature_celsius'].mean():.1f}°C", "temperature_celsius"),
        ("Risk Score", f"{f_df['Risk_Score'].mean():.2f}", "Risk_Score"),
        ("Total Rain", f"{f_df['precip_mm'].sum()/1e3:.1f}k", "precip_mm"),
        ("Wind Avg", f"{f_df['wind_kph'].mean():.1f}", "wind_kph"),
        ("Extreme Events", f"{f_df['Extreme_Event'].sum()}", "Extreme_Event"),
        ("Danger Hub", hub_name, "Risk_Score")
    ]
    for i, (l, v, c) in enumerate(k_metrics):
        with k_cols[i]:
            if i < 5: kpi_sparkline(l, v, f_df.groupby('date')[c].mean().tail(30))
            else: kpi_basic(l, v)

    st.markdown("### 🗺️ Planetary Geospatial View")
    toggle = st.radio("Choose map parameter:", ["Temperature", "Rainfall", "Risk Score"], horizontal=True)
    v_map = {"Temperature": "temperature_celsius", "Rainfall": "precip_mm", "Risk Score": "Risk_Score"}
    fig1 = px.choropleth(f_df.groupby("country")[v_map[toggle]].mean().reset_index(), locations="country", locationmode="country names", color=v_map[toggle], color_continuous_scale="Turbo")
    fig1.update_geos(showcoastlines=True, coastlinecolor="white")
    apply_viz(fig1, f"World Weather Map: {toggle}", "The map shows which parts of the world are facing the most heat or rain right now.")

    t_multi = f_df.set_index('date').resample('M')[['temperature_celsius', 'precip_mm', 'Risk_Score']].mean().reset_index()
    for col in ['temperature_celsius', 'precip_mm', 'Risk_Score']:
        den = (t_multi[col].max() - t_multi[col].min())
        t_multi[col] = (t_multi[col] - t_multi[col].min()) / den if den != 0 else 0
    fig2 = px.line(t_multi, x="date", y=['temperature_celsius', 'precip_mm', 'Risk_Score'], markers=True)
    apply_viz(fig2, "World Weather Trends", "By looking at the trends, we can see that heat and environmental risks are rising together over time.")

    top5 = f_df.groupby("country")["temperature_celsius"].mean().nlargest(5).reset_index().assign(Category='Top 5 Hot')
    bot5 = f_df.groupby("country")["temperature_celsius"].mean().nsmallest(5).reset_index().assign(Category='Top 5 Cool')
    apply_viz(px.bar(pd.concat([top5, bot5]), x="country", y="temperature_celsius", color="Category", color_discrete_map={'Top 5 Hot':'#ef4444', 'Top 5 Cool':'#3b82f6'}), "Hottest and Coldest Countries", "This list helps us quickly compare the countries with the highest and lowest temperatures.")

# ==========================================================
# 🌡️ 2. TEMPERATURE ANALYSIS
# ==========================================================
elif selected == "Temperature Analysis":
    st.markdown("<h1 style='color:#FFFFFF;'>🌡️ TEMPERATURE TRENDS</h1>", unsafe_allow_html=True)
    top_n = st.slider("Select number of countries to rank", 3, 10, 5)
    
    k_cols = st.columns(4)
    with k_cols[0]: kpi_basic("Hottest Record", f"{f_df['temperature_celsius'].max():.1f}°C")
    with k_cols[1]: kpi_basic("Coldest Record", f"{f_df['temperature_celsius'].min():.1f}°C")
    with k_cols[2]: kpi_basic("Temp Change", f"{(f_df['temperature_celsius'].mean() - df['temperature_celsius'].mean()):.2f}")
    with k_cols[3]: kpi_basic("Volatility", f"{f_df['temperature_celsius'].std():.2f}")

    apply_viz(px.imshow(f_df.groupby(["year", "month"])["temperature_celsius"].mean().unstack(), text_auto=".1f", color_continuous_scale="YlOrRd"), "Yearly Heat Calendar", "The heat calendar shows that summers are now lasting longer and becoming more intense every year.")
    apply_viz(px.histogram(f_df, x="temperature_celsius", color="country" if country_sel else None, marginal="violin", barmode='overlay'), "Common Temperature Ranges", "We are seeing more extremely hot days now compared to what was normal in the past.")
    
    top_c = f_df.groupby("country")["temperature_celsius"].mean().nlargest(top_n).index
    apply_viz(px.line(f_df[f_df['country'].isin(top_c)].groupby(['date', 'country'])['temperature_celsius'].mean().reset_index(), x='date', y='temperature_celsius', color='country'), f"Warming Trends in Top {top_n} Hotspots", "In the world’s hottest areas, temperatures are rising much faster than the global average.")
    apply_viz(px.violin(f_df, y="temperature_celsius", x="country" if country_sel else None, color="country" if country_sel else None, box=True, points="all"), "How Temperatures Vary by Region", "Some countries have very steady weather, while others face wild and unpredictable temperature swings.")

# ==========================================================
# 🌧️ 3. RAINFALL & WIND
# ==========================================================
elif selected == "Rainfall & Wind":
    st.markdown("<h1 style='color:#FFFFFF;'>🌧️ RAIN & WIND PATTERNS</h1>", unsafe_allow_html=True)
    top_n_rain = st.slider("Select number of countries for rain ranking", 3, 10, 5)
    
    k_cols = st.columns(4)
    with k_cols[0]: kpi_basic("Total Rain", f"{f_df['precip_mm'].sum():,.0f} mm")
    with k_cols[1]: kpi_basic("Heavy Rain Days", (f_df["precip_mm"] > 100).sum())
    with k_cols[2]: kpi_basic("Avg Wind Speed", f"{f_df['wind_kph'].mean():.2f}")
    with k_cols[3]: kpi_basic("Strongest Wind", f"{f_df['wind_kph'].max():.1f}")

    top_rc = f_df.groupby("country")["precip_mm"].sum().nlargest(top_n_rain).index
    apply_viz(px.line(f_df[f_df['country'].isin(top_rc)].groupby(['date', 'country'])['precip_mm'].sum().reset_index(), x="date", y="precip_mm", color="country", markers=True), "Rainfall Patterns Over Time", "Sudden spikes in these lines show exactly when and where heavy floods are most likely to happen.")
    
    w_tr = f_df.set_index('date').resample('M')['wind_kph'].mean().reset_index()
    w_tr['Smooth'] = w_tr['wind_kph'].rolling(window=3).mean()
    apply_viz(px.line(w_tr, x='date', y=['wind_kph', 'Smooth'], color_discrete_map={'wind_kph': 'rgba(255,255,255,0.2)', 'Smooth': '#10b981'}), "Wind Speed Trends", "Even after removing seasonal noise, we can see that the air is carrying more energy and stronger winds.")
    apply_viz(px.scatter(f_df, x="precip_mm", y="wind_kph", trendline="ols", color="temperature_celsius"), "Rain vs. Wind Connection", "Generally, when the wind gets stronger, we see a clear increase in the amount of rainfall.")
    apply_viz(px.bar(f_df.groupby("country")["precip_mm"].sum().nlargest(10).reset_index().sort_values("precip_mm"), y="country", x="precip_mm", orientation='h', color="precip_mm", color_continuous_scale="Blues"), "Countries with Most Rain", "This ranking shows which countries handle the most water and are at higher risk for soil damage.")

# ==========================================================
# 🚨 4. EXTREME EVENTS
# ==========================================================
elif selected == "Extreme Events":
    st.markdown("<h1 style='color:#FFFFFF;'>🚨 WEATHER EMERGENCIES</h1>", unsafe_allow_html=True)
    k_cols = st.columns(4)
    with k_cols[0]: kpi_basic("Total Heatwaves", (f_df["temperature_celsius"] > 40).sum())
    with k_cols[1]: kpi_basic("Total Floods", (f_df["precip_mm"] > 100).sum())
    with k_cols[2]: kpi_basic("Total Storms", (f_df["wind_kph"] > 60).sum())
    with k_cols[3]: kpi_basic("Emergency Hub", f_df.groupby("country")["Extreme_Event"].sum().idxmax() if not f_df.empty else "N/A")

    apply_viz(px.pie(pd.DataFrame({"Event":["Heat", "Rain", "Wind"], "Count":[(f_df["temperature_celsius"]>40).sum(), (f_df["precip_mm"]>100).sum(), (f_df["wind_kph"]>60).sum()]}), values="Count", names="Event", hole=0.6, color_discrete_sequence=px.colors.sequential.RdBu), "Types of Dangerous Weather", "Heatwaves are currently the most frequent type of dangerous weather event happening globally.")
    
    tl_h = f_df.groupby("date")["Extreme_Event"].sum().reset_index()
    tl_h["Cum"] = tl_h["Extreme_Event"].cumsum()
    apply_viz(px.line(tl_h, x="date", y="Cum"), "Total Weather Emergencies Over Time", "The rising line shows that weather emergencies are happening more often, leaving less time for countries to recover.")
    apply_viz(px.imshow(f_df.groupby(["year", "month"])["Extreme_Event"].sum().unstack(), text_auto=True, color_continuous_scale="Reds"), "Dangerous Months Matrix", "This grid helps us predict which months are most likely to have multiple dangerous weather events at once.")
    apply_viz(px.bar(f_df.groupby("country")["Extreme_Event"].sum().nlargest(10).reset_index().sort_values("Extreme_Event"), x="Extreme_Event", y="country", color="Extreme_Event", color_continuous_scale="OrRd"), "Countries Facing Most Emergencies", "Some countries are now stuck in a cycle of constant weather emergencies that affect their daily life.")

# ==========================================================
# 🌐 5. COUNTRY COMPARISON
# ==========================================================
elif selected == "Country Comparison":
    st.markdown("<h1 style='color:#FFFFFF;'>⚖️ COMPARE TWO COUNTRIES</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: ca = st.selectbox("Select First Country", countries_list, index=0)
    with c2: cb = st.selectbox("Select Second Country", [c for c in countries_list if c != ca], index=0)
    dfa, dfb = f_df[f_df["country"] == ca].sort_values('date'), f_df[f_df["country"] == cb].sort_values('date')
    
    k_comp = st.columns(4)
    with k_comp[0]: kpi_basic("Temp Difference", f"{(dfa['temperature_celsius'].mean() - dfb['temperature_celsius'].mean()):+.2f}°C")
    with k_comp[1]: kpi_basic("Risk Gap %", f"{(dfa['Risk_Score'].mean() - dfb['Risk_Score'].mean())*100:+.1f}%")
    with k_comp[2]: kpi_basic("Rainfall Gap", f"{(dfa['precip_mm'].sum() - dfb['precip_mm'].sum()):+,.0f} mm")
    with k_comp[3]: kpi_basic("Sun Intensity Gap", f"{(dfa['uv_index'].mean() - dfb['uv_index'].mean()):+.1f}")

    r_cats = ['Temp', 'Humidity', 'Wind', 'Sun', 'Visibility']
    def get_r(s):
        m = [s[col].mean() for col in ['temperature_celsius', 'humidity', 'wind_kph', 'uv_index', 'visibility_km']]
        mx = [df[col].max() if df[col].max() != 0 else 1 for col in ['temperature_celsius', 'humidity', 'wind_kph', 'uv_index', 'visibility_km']]
        return [v / mv for v, mv in zip(m, mx)]
    
    fig16 = go.Figure()
    fig16.add_trace(go.Scatterpolar(r=get_r(dfa), theta=r_cats, fill='toself', name=ca))
    fig16.add_trace(go.Scatterpolar(r=get_r(dfb), theta=r_cats, fill='toself', name=cb))
    fig16.update_traces(opacity=0.6)
    apply_viz(fig16, "Climate Personality Comparison", "This 'fingerprint' chart shows how one country might be 'Hot and Dry' while the other is 'Rainy and Windy'.")

    dfa['c_rain'] = dfa['precip_mm'].cumsum(); dfb['c_rain'] = dfb['precip_mm'].cumsum()
    apply_viz(px.area(pd.concat([dfa, dfb]), x='date', y='c_rain', color='country'), "Total Yearly Rainfall Gap", "This graph clearly shows the big difference in how much total water each country receives in a year.")

    comb_ab = pd.concat([dfa, dfb]).dropna(subset=['uv_index','cloud'])
    model = sm.OLS(comb_ab['uv_index'], sm.add_constant(comb_ab['cloud'])).fit()
    apply_viz(px.scatter(comb_ab, x="cloud", y="uv_index", color="country", trendline="ols"), f"Sun Intensity vs. Clouds | y={model.params[1]:.3f}x+{model.params[0]:.3f}", "We can see exactly how well clouds in different regions help block out harmful sun rays.")

# ==========================================================
# 🛡️ 6. RISK INDEX
# ==========================================================
elif selected == "Risk Index":
    st.markdown("<h1 style='color:#FFFFFF;'>🛡️ WORLD SAFETY SCORE</h1>", unsafe_allow_html=True)
    
    k_r = st.columns(4)
    with k_r[0]: kpi_sparkline("Global Safety", f"{f_df['Risk_Score'].mean():.2f}", f_df.groupby('date')['Risk_Score'].mean().tail(30))
    with k_r[1]: kpi_basic("Danger Hub", hub_name)
    with k_r[2]: kpi_basic("Risk Speed", f"{f_df.groupby('year')['Risk_Score'].mean().pct_change().mean()*100:+.2f}%")
    with k_r[3]: kpi_basic("Risk Variation", f"{f_df['Risk_Score'].std():.2f}")

    fig19 = go.Figure(go.Indicator(mode = "gauge+number", value = f_df['Risk_Score'].mean(), title = {'text': "Global Safety Score"},
        gauge = {'axis': {'range': [0, 1]}, 'bar': {'color': "#10b981"}, 'steps' : [{'range': [0, 0.5], 'color': "#30363D"}, {'range': [0.5, 1], 'color': "#ef4444"}]}))
    fig19.update_layout(font=dict(size=16), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig19, use_container_width=True)
    st.markdown('<div class="insight-block"><b>PRESENTATION INSIGHT:</b> The safety dial shows the overall danger level by combining heat, wind, and rain data into one score.</div>', unsafe_allow_html=True)

    corr_m = f_df[['temperature_celsius', 'precip_mm', 'wind_kph', 'Risk_Score', 'humidity', 'uv_index']].corr()
    apply_viz(px.imshow(corr_m.where(~np.triu(np.ones_like(corr_m, dtype=bool))), text_auto=".2f", color_continuous_scale="RdBu_r"), "What Drives Climate Risk?", "Heat and sun intensity are the two biggest factors making our world more dangerous right now.")
    
    r_tr = f_df.set_index('date').resample('M')['Risk_Score'].mean().reset_index()
    r_tr['Smooth'] = r_tr['Risk_Score'].rolling(3).mean()
    apply_viz(px.line(r_tr, x='date', y=['Risk_Score', 'Smooth'], color_discrete_map={'Risk_Score': 'rgba(255,255,255,0.2)', 'Smooth': '#ef4444'}), "Risk Levels Rising Over Time", "Climate risks aren't just jumping around—they are steadily moving into a more dangerous zone every year.")
    
    top10_r = f_df.groupby("country")["Risk_Score"].mean().nlargest(10).reset_index().sort_values("Risk_Score")
    fig22 = px.bar(top10_r, x="Risk_Score", y="country", orientation='h')
    colors = ['#64748b'] * len(top10_r)
    for i in range(len(top10_r)-3, len(top10_r)): colors[i] = '#10b981'
    fig22.update_traces(marker_color=colors)
    apply_viz(fig22, "Top 10 High-Risk Areas", "These 10 countries are the most vulnerable and need the most help to prepare for future weather changes.")

# ==========================================================
# 🏁 FOOTER
# ==========================================================
st.divider()
st.caption("Climate Intelligence Enterprise | High-Fidelity Infinity Engine v16.1 © 2026")