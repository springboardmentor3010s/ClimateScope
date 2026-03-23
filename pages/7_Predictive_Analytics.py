import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# We use scipy for basic poly-fitting confidence intervals
from scipy import stats

from app import load_data, load_css, global_filters, render_kpi, section_header, make_chart_layout

def main():
    load_css()
    df = load_data()
    # Force 'date' to datetime
    df["date"] = pd.to_datetime(df["date"])

    df_filt, country_sel, year_range = global_filters(df)

    st.markdown(
        """
        <div class="page-title">📈 Predictive Climate Analytics</div>
        <div class="page-subtitle">
            Machine Learning forecasting of temperature trajectories and extreme event probability models.
        </div>
        <div class="accent-line"></div>
        """,
        unsafe_allow_html=True,
    )

    if df_filt.empty:
        st.warning("Insufficient data for predictive modeling.")
        return

    # ---------- ML Forecast Settings ----------
    section_header("⚙️", "Forecast Parameters")
    
    with st.container():
        st.markdown(
            '<div class="glass-panel" style="padding:1rem;">'
            '<div style="font-weight:600; color:var(--text-color); margin-bottom:0.5rem;">Forecast Horizon (Months)</div>',
            unsafe_allow_html=True
        )
        forecast_months = st.slider("Predict future months", min_value=12, max_value=60, value=24, step=12)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Temperature Trajectory Model ----------
    section_header("🌡️", "Temperature Trajectory Forecasting")
    
    # 1. Prepare Time Series
    ts = df_filt.groupby(df_filt["date"].dt.to_period("M"))["temperature_celsius"].mean().reset_index()
    ts["date"] = ts["date"].dt.to_timestamp()
    ts = ts.dropna().sort_values("date")
    
    if len(ts) < 12:
        st.error("Need at least 12 months of historical data to build a reliable forecast model.")
        return

    # 2. Build Polynomial Regression Model with SciPy
    # Use ordinal dates for regression
    x = ts["date"].apply(lambda d: d.toordinal()).values
    y = ts["temperature_celsius"].values
    
    # Fit 2nd degree polynomial (captures acceleration in warming better than linear)
    degree = 2
    coeffs = np.polyfit(x, y, degree)
    poly_model = np.poly1d(coeffs)
    
    # Historical Fit
    ts["trend_fit"] = poly_model(x)
    
    # Forecast Generation
    last_date = ts["date"].max()
    future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, forecast_months + 1)]
    future_x = np.array([d.toordinal() for d in future_dates])
    future_y = poly_model(future_x)
    
    # Confidence Interval simulation (using standard error of the regression)
    residuals = y - ts["trend_fit"]
    s_err = np.std(residuals)
    
    # Expanding cone of uncertainty
    t_val = stats.t.ppf(0.975, df=len(x)-degree-1) # 95% CI
    uncertainty_growth = np.linspace(1.2, 2.5, len(future_x)) # Cone expands over time
    ci_upper = future_y + (t_val * s_err * uncertainty_growth)
    ci_lower = future_y - (t_val * s_err * uncertainty_growth)

    # ---------- Visualize Temperature Model ----------
    fig_pred = go.Figure()
    
    # Historical Data
    fig_pred.add_trace(go.Scatter(
        x=ts["date"], y=ts["temperature_celsius"],
        mode="lines", name="Historical Avg",
        line=dict(color="#3b82f6", width=2, dash="dot"),
        opacity=0.6
    ))
    
    # Historical Trend Fit
    fig_pred.add_trace(go.Scatter(
        x=ts["date"], y=ts["trend_fit"],
        mode="lines", name="Model Fit",
        line=dict(color="#6366f1", width=3)
    ))
    
    # Future Forecast
    fig_pred.add_trace(go.Scatter(
        x=future_dates, y=future_y,
        mode="lines", name="Forecast",
        line=dict(color="#f59e0b", width=3, dash="dash")
    ))
    
    # Confidence Intervals (Shaded Area)
    fig_pred.add_trace(go.Scatter(
        x=list(future_dates) + list(future_dates)[::-1],
        y=list(ci_upper) + list(ci_lower)[::-1],
        fill="toself",
        fillcolor="rgba(245, 158, 11, 0.15)",
        line=dict(color="rgba(255,255,255,0)"),
        hoverinfo="skip",
        name="95% Confidence Interval"
    ))
    
    make_chart_layout(fig_pred, height=500)
    fig_pred.update_layout(
        xaxis_title="Timeline", yaxis_title="Temperature (°C)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_pred, use_container_width=True, config={"displayModeBar": False})

    # ---------- KPIs from the Model ----------
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi("Forecast Horizon", f"+{forecast_months} Months", meta="Model depth")
    with col2:
        current_temp = y[-1]
        projected_temp = future_y[-1]
        delta = projected_temp - current_temp
        render_kpi("Projected Shift", f"{delta:+.2f} °C", meta=f"By end of forecast", meta_is_positive=(delta<0))
    with col3:
        risk_likelihood = "High" if delta > 0.5 else ("Medium" if delta > 0.1 else "Stable")
        render_kpi("Systemic Risk Probability", risk_likelihood, meta="Based on trajectory", meta_is_positive=(risk_likelihood=="Stable"))
        
    if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
        st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
        st.session_state.kpi_buffer = []

    # ---------- Extreme Event Extrapolation ----------
    section_header("🚨", "Extreme Event Probability Modeling")
    
    # Calculate probability of extreme events based on historical rolling occurrences
    ee_ts = df_filt.groupby(df_filt["date"].dt.to_period("M"))["has_extreme_event"].mean().reset_index()
    ee_ts["date"] = ee_ts["date"].dt.to_timestamp()
    
    fig_prob = px.area(
        ee_ts, x="date", y="has_extreme_event",
        color_discrete_sequence=["#ef4444"],
    )
    fig_prob.update_traces(
        line=dict(width=2, color="#ef4444"),
        fillcolor="rgba(239, 68, 68, 0.1)",
        hovertemplate="%{x|%b %Y}<br>Prob: %{y:.2%}<extra></extra>"
    )
    make_chart_layout(fig_prob, height=350)
    fig_prob.add_hline(y=ee_ts["has_extreme_event"].mean(), line_dash="dash", line_color="#f59e0b", annotation_text="Historical Avg Probability")
    fig_prob.update_layout(xaxis_title="Date", yaxis_title="Base Probability (%)", yaxis_tickformat=".1%")
    
    st.plotly_chart(fig_prob, use_container_width=True, config={"displayModeBar": False})

if __name__ == "__main__":
    main()
