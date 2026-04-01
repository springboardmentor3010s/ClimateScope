🌍 ClimateScope: Visualizing Global Weather Trends and Extreme Events
📌 Project Overview

ClimateScope is a data analytics project focused on analyzing and visualizing global weather patterns using real-world data. The project transforms raw weather data into meaningful insights through data preprocessing, statistical analysis, and interactive dashboards.

The goal is to understand climate behavior, identify trends, and highlight extreme weather conditions across different regions.

🎯 Objectives
Analyze global weather data and identify climate patterns
Perform data cleaning and preprocessing using Python
Conduct statistical and correlation analysis
Build interactive dashboards using Tableau
Identify seasonal trends and extreme weather events
📂 Dataset
Source: Global Weather Repository (Kaggle)
Type: Time-series weather dataset
Records: 123,000+
Features: 41 columns
Key Variables:
Temperature (°C)
Humidity (%)
Wind Speed (kph)
Precipitation (mm)
Pressure (mb)
UV Index
Date & Time
🧹 Data Processing

Performed using Python (Pandas & NumPy):

Removed duplicate records
Handled invalid values (-9999 → NaN)
Filtered unrealistic values
Converted date column to datetime
Dropped redundant columns (unit duplicates)
Created time-based features (year, month)
📊 Statistical Analysis
Distribution analysis using quantiles
Correlation analysis between variables
Monthly and yearly trend analysis
Country-wise comparison
Extreme weather detection using 95th percentile
📈 Data Visualization (Tableau)

Developed 7 interactive dashboards:

Overview Dashboard – Key KPIs and global trends
Temperature Analysis – Seasonal trends & extremes
Rainfall Analysis – Distribution & regional patterns
Humidity Analysis – Variation across regions
Pressure Analysis – Stability and trends
UV Index Analysis – Relationship with temperature
Insights Dashboard – Correlation and key findings
🔍 Key Insights
Global average temperature ≈ 21.7°C
Rainfall is highly skewed (mostly low, few extreme events)
Strong relationships observed:
Temperature ↑ → UV ↑
Rainfall ↑ → Humidity ↑
Clear seasonal patterns in climate variables
Significant regional climate differences
🛠️ Tech Stack
Programming Language: Python 3
Libraries: Pandas, NumPy
Visualization Tool: Tableau
Dataset Source: Kaggle
📊 Project Workflow
Data Acquisition
Data Understanding
Data Cleaning & Preprocessing
Statistical Analysis
Data Visualization
Insights Generation
🎯 Conclusion

This project demonstrates how data analytics can be used to understand complex climate patterns. By combining Python and Tableau, raw weather data was transformed into actionable insights, helping in better understanding of global environmental conditions.

🚀 Future Scope
Integration with live weather APIs
Predictive modeling for forecasting
Real-time dashboard deployment
Advanced anomaly detection

👩‍💻 Author
Name: Gangalakshmi Raja
Project: Infosys Internship – ClimateScope