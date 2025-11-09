# forecast_dashboard.py
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# 🔗 Your Render API endpoint
API_URL = "https://mlp-0tnk.onrender.com/forecast"

# 🎨 Streamlit page setup
st.set_page_config(page_title="Energy Forecast Dashboard", layout="wide")
st.title("⚡ Energy Consumption Forecast Dashboard")

st.markdown("""
This dashboard fetches data from your deployed API and visualizes predicted energy consumption.
""")

# 📅 User input
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Select Start Date")
with col2:
    end_date = st.date_input("Select End Date")

# 🚀 Fetch data from API
if st.button("Get Forecast"):
    if not start_date or not end_date:
        st.warning("Please select both start and end dates.")
    else:
        params = {"start_date": str(start_date), "end_date": str(end_date)}
        try:
            response = requests.get(API_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)

                if df.empty:
                    st.warning("No data returned for the given range.")
                else:
                    st.subheader("📊 Forecast Data")
                    st.dataframe(df, use_container_width=True)

                    # 📈 Plot
                    st.subheader("📈 Predicted Energy Consumption (Avg KWh)")
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(df["Report_Date"], df["Predicted_Avg_Kwh"], marker="o")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Predicted Avg KWh")
                    ax.grid(True)
                    st.pyplot(fig)
            else:
                st.error(f"API Error: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
