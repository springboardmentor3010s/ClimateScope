# import pandas as pd

# def load_data():
#     df = pd.read_csv("data/cleaned_weather_monthly.csv")
#     return df

import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Load and preprocess the cleaned weather dataset.
    Caching improves dashboard performance.
    """

    # Load dataset
    df = pd.read_csv("data/cleaned_weather_monthly.csv")
 # Country → Continent mapping
    continent_map = {
        "Afghanistan": "Asia",
        "India": "Asia",
        "China": "Asia",
        "Japan": "Asia",
        
        "France": "Europe",
        "Germany": "Europe",
        "Italy": "Europe",
        "Spain": "Europe",
        
        "United States": "North America",
        "Canada": "North America",
        "Mexico": "North America",
        
        "Brazil": "South America",
        "Argentina": "South America",
        "Chile": "South America",
        
        "Australia": "Oceania",
        "New Zealand": "Oceania",
        
        "South Africa": "Africa",
        "Egypt": "Africa",
        "Nigeria": "Africa"
    }

    df["continent"] = df["country"].map(continent_map)

    # Ensure correct datatypes
    df["year"] = df["year"].astype(int)
    df["month"] = df["month"].astype(int)

    # Optional: create month name column for better charts
    month_map = {
        1:"Jan",2:"Feb",3:"Mar",4:"Apr",
        5:"May",6:"Jun",7:"Jul",8:"Aug",
        9:"Sep",10:"Oct",11:"Nov",12:"Dec"
    }

    df["month_name"] = df["month"].map(month_map)

    return df