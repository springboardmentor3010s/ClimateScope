import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Climate Intelligence Dashboard", layout="wide")

st.title("🌍 Global Climate Intelligence Dashboard")

st.markdown("""
This dashboard analyzes **global weather patterns** including temperature, rainfall, wind speed and climate risk indicators.

Use the **navigation panel on the left** to explore different analytical views of the dataset.

The dashboard includes:

• Executive Overview  
• Temperature Intelligence  
• Precipitation & Wind Analysis  
• Extreme Events Monitoring  
• Regional Climate Comparison  
• Climate Risk Intelligence
""")

df = pd.read_csv("/Users/garikapatiaishwarya/Desktop/climatescope/data/processed/global_weather_cleaned_daily.csv")

st.subheader("Dataset Preview")

st.write("""
The dataset contains global weather observations including temperature, precipitation, wind speed, and geographic coordinates.
""")

st.dataframe(df.head())