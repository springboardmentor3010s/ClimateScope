# ClimateScope: Visualizing Global Weather Trends and Extreme Events

## Problem Statement

As climate data grows in volume and complexity, there is a critical need for accessible platforms that translate raw numbers into actionable insights. Standard spreadsheets are no longer sufficient for spotting crucial environmental patterns.

The primary objective of this project is to analyze and visually represent global weather patterns using the comprehensive Global Weather Repository dataset. This project aims to uncover seasonal trends, regional variations, and extreme weather events through an interactive dashboard, providing a data-driven platform that supports climate awareness, informed decision-making, and further research into global weather dynamics.

## Key Questions Analyzed
To address the core objective, this dashboard specifically analyzes the following critical questions:

1. **Global Extremes** : 
    What are the absolute maximum and minimum temperatures, and which cities/countries experience them?

2. **Seasonal Trends** :
     How do temperature, humidity, and wind speed fluctuate across different months and quarters globally?

3.  **Precipitation Dynamics** :
     Which regions are most susceptible to heavy rainfall and severe wind velocities?

4. **Risk & Anomaly Tracking** :
     How frequent are extreme weather events (heatwaves, heavy rain, high winds), and which countries fall into the "High Risk" climate category?

# Dashboard Snapshot (Power BI Desktop)

![Global Event Dashboard](https://github.com/user-attachments/assets/6fe15c26-2b8e-4d3b-a49b-1e843f5f27b5)
## Steps Followed
- Step 1: Downloaded the Global Weather Repository dataset from Kaggle via the Kaggle API.

- Step 2: Set up the Python environment and loaded the dataset using pandas to inspect the structure, data types, and key variables (temperature, humidity, precipitation, etc.).

- Step 3: Performed Data Cleaning. Identified missing values and anomalies. Handled inconsistent entries and dropped nulls where necessary to ensure data accuracy.

- Step 4: Data Transformation. Aggregated the daily weather data into monthly and quarterly averages to improve processing efficiency and visualize long-term trends smoothly.

- Step 5: Conducted core statistical analysis to understand distributions, variable correlations, and pinpoint extreme weather events.

- Step 6: Designed the dashboard layout and selected appropriate visualization types (Choropleth maps for geography, Line charts for time-series, Bar charts for comparisons).

- Step 7: Built the interactive visualizations using Plotly. Created charts for Temperature Trends, Precipitation by Country, and a global Risk Category map.

- Step 8: Deployed the final interactive dashboard using Streamlit, integrating user controls like date sliders, country drop-downs, and city filters for dynamic data exploration.

## 📸 Dashboard Visuals & Analysis

### 1. Global Risk Map

Visualizing countries based on their calculated climate risk categories (High, Medium, Low).
![Global Risk Map](https://github.com/user-attachments/assets/3efb67e3-1441-44ec-b48a-cbd64f05d980)

### 2. Extreme Weather Events & Risk Score

Tracking total extreme events (Heatwaves, Heavy Rain, High Winds) and the distribution of Climate Risk Scores.
![Extreme Weather Events](https://github.com/user-attachments/assets/fdf206d8-a7f1-416e-84b7-14a9a7e65830)

### 3. Precipitation & Wind Trends

Analyzing total precipitation across countries and tracking maximum wind speeds by city.
![Precipitation and Wind Trends](https://github.com/user-attachments/assets/25cb52fa-df21-456c-b434-a1625154cd37)

### 4. Temperature Extremes by City & Country

Highlighting the absolute maximum and minimum temperatures recorded across various geographic locations.
![Temperature Trends](https://github.com/user-attachments/assets/d7ec4218-7621-47d8-bb17-5a0e9ee29998)

### 5. Overall Weather Trends

Detailed breakdown of average temperature, humidity, wind speed, and precipitation over time.
![Weather Trends Overview](https://github.com/user-attachments/assets/f98f51fc-d8fc-409e-821d-2752105ce56b)

💡 Key Insights Derived
Based on the visual dashboards above, several crucial insights were identified:

[1] Key Performance Indicators (KPIs) & Extremes
Global Thresholds: The dataset recorded an absolute maximum temperature of 49°C and a minimum of -30°C.

Extreme Event Volume: The dashboard successfully tracked 1,276 total extreme weather events during the measured period, heavily dominated by Heatwave Days (1,228), followed by High Wind Events (38) and Heavy Rain Events (10).

[2] Temperature Trends
The Hotspots: Middle Eastern countries consistently recorded the highest maximum temperatures, with Kuwait, Iraq, Djibouti, and Saudi Arabia frequently hitting the 46°C - 49°C range.

Seasonal Curves: The global average temperature trends follow a distinct bell curve, peaking globally during June, July, and August (~26°C average) before dipping toward the end of the year.

[3] Precipitation & Wind Dynamics
Tropical Rainfall: Total precipitation metrics highlight that tropical nations bear the brunt of global rainfall, with Brunei (612mm), Indonesia, and Malaysia leading the charts.

Wind Velocity: City-level wind tracking identified specific high-risk zones for storms, with Suva recording maximum wind speeds of up to 172 kph.

[4] Climate Risk Profiling
Global Vulnerability: By calculating a "Climate Risk Score," the interactive map categorizes regions into High, Medium, and Low risk. The pie chart distribution reveals that while ~81% of the data falls into lower risk scores, specific geographic clusters require critical monitoring for extreme climate shifts.
