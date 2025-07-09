import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load your trained model and features
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("features.pkl", "rb") as f:
        features = pickle.load(f)
except FileNotFoundError:
    st.error("🚫 model.pkl or features.pkl not found! Please make sure they're in the same folder as app.py.")
    st.stop()

# App Configuration
st.set_page_config(page_title="Dynamic Pricing Predictor", page_icon="💸", layout="centered")
st.title("💸 Dynamic Pricing Strategy Predictor")
st.markdown("""
Welcome! This tool helps you **predict optimal pricing** for your product or listing using machine learning.
Adjust the values in the sidebar to get a price prediction.
""")

# Sidebar Inputs
st.sidebar.header("🔧 Input Parameters")

location = st.sidebar.selectbox("📍 Location", ["Boston", "Chicago", "Miami", "Seattle", "Los Angeles"])
listing_type = st.sidebar.selectbox("🏨 Listing Type", ["Airbnb", "Hostel"])
day_of_week = st.sidebar.selectbox("📅 Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
season = st.sidebar.selectbox("🌤️ Season", ["Winter", "Spring", "Summer", "Fall"])
event = st.sidebar.selectbox("🎉 Event Nearby?", ["Yes", "No"])

base_price = st.sidebar.number_input("💰 Base Price (₹)", min_value=50.0, max_value=500.0, value=200.0, step=10.0)
demand_index = st.sidebar.slider("📈 Demand Index", 0.0, 1.0, 0.5, step=0.01)
competitor_avg_price = st.sidebar.number_input("📊 Competitor Average Price (₹)", 50.0, 600.0, 250.0, step=10.0)
occupancy_rate = st.sidebar.slider("🏘️ Occupancy Rate (%)", 0.0, 100.0, 70.0, step=1.0)
customer_rating = st.sidebar.slider("⭐ Customer Rating", 0.0, 5.0, 3.5, step=0.1)
lead_time = st.sidebar.slider("📅 Lead Time (days)", 0, 60, 15)
weather_score = st.sidebar.slider("🌦️ Weather Score", 0.0, 1.0, 0.5, step=0.01)

# Prepare input dictionary
input_dict = {
    'base_price': base_price,
    'demand_index': demand_index,
    'competitor_avg_price': competitor_avg_price,
    'occupancy_rate': occupancy_rate,
    'customer_rating'_

