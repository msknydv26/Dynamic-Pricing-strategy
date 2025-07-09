import streamlit as st
import pandas as pd
import numpy as np
import pickle
import traceback

st.set_page_config(page_title="Dynamic Pricing Predictor", page_icon="💸", layout="centered")
st.title("💸 Dynamic Pricing Strategy Predictor")
st.markdown("Enter listing details to predict the final optimal price using our trained ML model.")

# --- Load model and features safely ---
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("features.pkl", "rb") as f:
        features = pickle.load(f)
except Exception as e:
    st.error("❌ Failed to load model or features.")
    st.code(traceback.format_exc())
    st.stop()

# --- Sidebar Inputs ---
st.sidebar.header("📋 Input Parameters")

location = st.sidebar.selectbox("📍 Location", ["Boston", "Chicago", "Miami", "Seattle", "Los Angeles"])
listing_type = st.sidebar.selectbox("🏨 Listing Type", ["Airbnb", "Hostel"])
day_of_week = st.sidebar.selectbox("📅 Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
season = st.sidebar.selectbox("🌤️ Season", ["Winter", "Spring", "Summer", "Fall"])
event = st.sidebar.selectbox("🎉 Event Nearby?", ["Yes", "No"])

base_price = st.sidebar.number_input("💰 Base Price (₹)", 50.0, 500.0, 200.0)
demand_index = st.sidebar.slider("📈 Demand Index", 0.0, 1.0, 0.5)
competitor_avg_price = st.sidebar.number_input("📊 Competitor Avg Price (₹)", 50.0, 600.0, 250.0)
occupancy_rate = st.sidebar.slider("🏘_
