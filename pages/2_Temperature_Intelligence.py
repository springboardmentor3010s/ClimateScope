# import streamlit as st
# import plotly.express as px
# from prophet import Prophet
# from utils.load_data import load_data

# st.title("🌡 Temperature Intelligence Dashboard")

# df = load_data()

# # ---------------- FORECAST ----------------
# st.subheader("🔮 Temperature Forecast")

# forecast_df = df[["year","temperature_celsius"]]
# forecast_df = forecast_df.rename(columns={"year":"ds","temperature_celsius":"y"})

# model = Prophet()
# model.fit(forecast_df)

# future = model.make_future_dataframe(periods=5, freq='Y')
# forecast = model.predict(future)

# fig_forecast = px.line(forecast, x="ds", y="yhat", title="Future Temperature Prediction")
# st.plotly_chart(fig_forecast, use_container_width=True)

# # ---------------- HEATMAP ----------------
# st.subheader("🔥 Seasonal Heatmap")

# fig = px.density_heatmap(
#     df,
#     x="month",
#     y="year",
#     z="temperature_celsius"
# )

# st.plotly_chart(fig)

# # ---------------- ANOMALY ----------------
# st.subheader("🚨 Temperature Anomalies")

# df["z"] = (df["temperature_celsius"] - df["temperature_celsius"].mean()) / df["temperature_celsius"].std()
# anomaly = df[abs(df["z"]) > 2]

# st.write(anomaly)



import streamlit as st
import plotly.express as px
from prophet import Prophet
from utils.load_data import load_data

px.defaults.template = "plotly_dark"

st.title("🌡 Temperature Dashboard")

df = load_data()

# ---------------- FORECAST ----------------
forecast_df = df[["year","temperature_celsius"]]
forecast_df = forecast_df.rename(columns={"year":"ds","temperature_celsius":"y"})

model = Prophet()
model.fit(forecast_df)

future = model.make_future_dataframe(periods=5, freq='Y')
forecast = model.predict(future)

fig = px.line(forecast, x="ds", y="yhat", title="Forecast")
st.plotly_chart(fig)

# ---------------- ROLLING ----------------
df["rolling"] = df["temperature_celsius"].rolling(3).mean()

fig = px.line(df, x="month", y="rolling", color="country")
st.plotly_chart(fig)

# ---------------- MATRIX ----------------
fig = px.scatter_matrix(
    df,
    dimensions=["temperature_celsius","precip_mm","wind_kph","humidity"],
    color="country"
)
st.plotly_chart(fig)

# ---------------- ANOMALY ----------------
df["z"] = (df["temperature_celsius"]-df["temperature_celsius"].mean())/df["temperature_celsius"].std()
st.write(df[df["z"].abs()>2])