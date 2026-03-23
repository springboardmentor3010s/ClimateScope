import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app import load_data, load_css, global_filters, render_kpi, section_header, make_chart_layout

def generate_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a correlation matrix for key numerical variables."""
    numeric_cols = ["temperature_celsius", "humidity", "wind_kph", "precip_mm", "uv_index", "air_quality_pm2_5", "risk_score", "has_extreme_event"]
    cols_present = [c for c in numeric_cols if c in df.columns]
    return df[cols_present].corr()

def simulate_economic_impact(df: pd.DataFrame) -> dict:
    """Translate climate risk metrics into estimated business impacts."""
    # Base numbers
    avg_risk = df["risk_score"].mean() if "risk_score" in df.columns else 20.0
    total_extreme = df["has_extreme_event"].sum() if "has_extreme_event" in df.columns else 0
    avg_temp = df["temperature_celsius"].mean() if "temperature_celsius" in df.columns else np.nan
    
    # 1. Supply Chain Disruption Days (~1 day per extreme event, scaled by risk)
    supply_chain_days = int(total_extreme * (1 + (avg_risk / 100)))
    
    # 2. Infrastructure Exposure Risk ($M) - Simulated based on temp anomalies and extremes
    # Assume base infrastructure value at risk is $10M per country, scaling aggressively with risk
    infra_risk_m = float((avg_risk ** 1.5) * 0.1) + (total_extreme * 2.5)
    
    # 3. Agricultural Yield Volatility (%)
    # Heat and precip variance drives agricultural risk
    temp_std = df["temperature_celsius"].std() if not pd.isna(avg_temp) else 0.0
    precip_std = df["precip_mm"].std() if "precip_mm" in df.columns else 0.0
    ag_volatility = float((temp_std * 2.5) + (precip_std * 0.1))
    
    return {
        "supply_chain_days": min(supply_chain_days, 365),
        "infra_risk_m": infra_risk_m,
        "ag_volatility": min(ag_volatility, 100.0)
    }

def main():
    load_css()
    df = load_data()
    df_filt, country_sel, year_range = global_filters(df)

    st.markdown(
        """
        <div class="page-title">💼 Economic Impact Simulator</div>
        <div class="page-subtitle">
            Translate environmental and climate data into tangible enterprise risk models.
        </div>
        <div class="accent-line"></div>
        """,
        unsafe_allow_html=True,
    )

    if df_filt.empty:
        st.warning("Insufficient data for economic modeling.")
        return

    # ---------- Simulation Overview ----------
    section_header("⚙️", "Localized Impact Simulation")
    
    impacts = simulate_economic_impact(df_filt)
    
    st.markdown(f"**Simulation Target:** {country_sel} (Period: {year_range[0]} - {year_range[1]})")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi(
            "Supply Chain Disruptions",
            f"{impacts['supply_chain_days']} Days",
            meta="Est. logistical delays",
            meta_is_positive=(impacts['supply_chain_days'] < 30)
        )
    with col2:
        render_kpi(
            "Infrastructure Exposure",
            f"${impacts['infra_risk_m']:,.1f} M",
            meta="Capital at risk",
            meta_is_positive=(impacts['infra_risk_m'] < 50.0)
        )
    with col3:
        render_kpi(
            "Agri-Yield Volatility",
            f"{impacts['ag_volatility']:,.1f} %",
            meta="Crop output variance",
            meta_is_positive=(impacts['ag_volatility'] < 15.0)
        )
        
    if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
        st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
        st.session_state.kpi_buffer = []

    # ---------- Correlation Matrix ----------
    section_header("🧬", "Risk Factor Correlation Matrix")
    
    corr_df = generate_correlation_matrix(df_filt)
    
    if not corr_df.empty:
        st.markdown("<div style='color: var(--text-color); margin-bottom: 10px; font-weight: 500;'>Statistical correlation between primary variables</div>", unsafe_allow_html=True)
        # Use a contrasting colormap suitable for both dark and light
        # RdBu is excellent: Red for negative corr, Blue for positive corr
        fig_corr = px.imshow(
            corr_df,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdBu",
            zmin=-1, zmax=1
        )
        
        make_chart_layout(fig_corr, height=600)
        fig_corr.update_layout(
            margin=dict(t=10, l=10, r=10, b=10)
        )
        
        st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Insufficient numeric columns to compute correlations.")
        
    # ---------- Top Economic Risk Regions ----------
    if country_sel == "All":
        section_header("🌍", "Global Highest Economic Exposure")
        
        risk_table = []
        for c in df_filt["country"].unique():
            c_df = df_filt[df_filt["country"] == c]
            c_imp = simulate_economic_impact(c_df)
            risk_table.append({
                "Country": c,
                "Supply Disruptions (Days)": c_imp["supply_chain_days"],
                "Capital Risk ($M)": c_imp["infra_risk_m"],
                "Agri Volatility (%)": c_imp["ag_volatility"]
            })
            
        risk_df = pd.DataFrame(risk_table).sort_values("Capital Risk ($M)", ascending=False).head(10)
        
        # Display as a horizontal bar chart
        fig_bar = px.bar(
            risk_df, x="Capital Risk ($M)", y="Country", orientation='h',
            color="Capital Risk ($M)", color_continuous_scale="Reds"
        )
        make_chart_layout(fig_bar, height=450)
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

if __name__ == "__main__":
    main()
