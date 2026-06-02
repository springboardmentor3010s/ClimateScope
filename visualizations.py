import streamlit as st
import plotly.express as px
import pandas as pd

def show_charts(df):

    # ================= KPIs =================
    st.subheader("📊 Executive KPIs")

    avg_temp = df["temperature_celsius"].mean()
    avg_humidity = df["humidity"].mean()
    avg_wind = df["wind_kph"].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("🌡 Avg Temp", f"{avg_temp:.2f}°C")
    col2.metric("💧 Avg Humidity", f"{avg_humidity:.2f}%")
    col3.metric("🌬 Avg Wind", f"{avg_wind:.2f} km/h")
    col4.metric("🔥 Max Temp", f"{df['temperature_celsius'].max():.2f}°C")
    col5.metric("❄ Min Temp", f"{df['temperature_celsius'].min():.2f}°C")

    st.markdown("---")

    # ================= TABS =================
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Overview", "🌡 Temperature", "📈 Trends", "⚠ Risk Analysis", "🗺 Map"]
    )

    # ================= OVERVIEW =================
    with tab1:

        col1, col2 = st.columns(2)

        # Top 10 hottest countries
        top10 = df.groupby("country")["temperature_celsius"].mean().nlargest(10).reset_index()
        fig = px.bar(top10, x="country", y="temperature_celsius",
                     title="🔥 Top 10 Hottest Countries",
                     color="temperature_celsius")
        col1.plotly_chart(fig, use_container_width=True)

        # Top 10 humid countries
        humid = df.groupby("country")["humidity"].mean().nlargest(10).reset_index()
        fig2 = px.bar(humid, x="country", y="humidity",
                      title="💧 Top 10 Humid Countries",
                      color="humidity")
        col2.plotly_chart(fig2, use_container_width=True)

        # Distribution
        fig3 = px.histogram(df, x="temperature_celsius", nbins=30, title="Temperature Distribution")
        st.plotly_chart(fig3, use_container_width=True)

    # ================= TEMPERATURE =================
    with tab2:

        fig = px.scatter(
            df,
            x="temperature_celsius",
            y="humidity",
            color="condition_text",
            size="wind_kph",
            hover_name="location_name",
            title="Temperature vs Humidity"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Boxplot
        fig2 = px.box(df, x="country", y="temperature_celsius",
                      title="Temperature Spread by Country")
        st.plotly_chart(fig2, use_container_width=True)

    # ================= TRENDS =================
    with tab3:

        if "last_updated" in df.columns:
            df["last_updated"] = pd.to_datetime(df["last_updated"])
            df["year"] = df["last_updated"].dt.year

            yearly = df.groupby("year")["temperature_celsius"].mean().reset_index()

            fig = px.line(yearly, x="year", y="temperature_celsius",
                          markers=True, title="📈 Yearly Temperature Trend")
            st.plotly_chart(fig, use_container_width=True)

        # Correlation Heatmap
        corr = df[["temperature_celsius", "humidity", "wind_kph"]].corr()
        fig2 = px.imshow(corr, text_auto=True, title="Correlation Matrix")
        st.plotly_chart(fig2, use_container_width=True)

    # ================= RISK =================
    with tab4:

        st.subheader("🚨 Climate Risk Intelligence")

        col1, col2 = st.columns(2)

        # Top risk countries
        risk = df.groupby("country")["risk_score"].mean().nlargest(10).reset_index()
        fig = px.bar(risk, x="country", y="risk_score",
                     title="Top 10 Risk Countries",
                     color="risk_score")
        col1.plotly_chart(fig, use_container_width=True)

        # Risk distribution
        fig2 = px.pie(df, names="risk_level", title="Risk Distribution")
        col2.plotly_chart(fig2, use_container_width=True)

        # Extreme Events
        extreme = df[
            (df["temperature_celsius"] > 40) |
            (df["humidity"] > 90) |
            (df["wind_kph"] > 60)
        ]

        st.metric("⚠ Extreme Events", extreme.shape[0])
        st.dataframe(extreme)

    # ================= MAP =================
    with tab5:

        if "latitude" in df.columns:
            fig = px.scatter_mapbox(
                df,
                lat="latitude",
                lon="longitude",
                color="temperature_celsius",
                hover_name="location_name",
                zoom=1
            )
            fig.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig, use_container_width=True)