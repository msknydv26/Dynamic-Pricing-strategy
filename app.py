import streamlit as st
import pandas as pd
import pickle
import requests
import io

# --- App Title ---
st.set_page_config(page_title="Dynamic Price Predictor", layout="centered")
st.title("💸 Dynamic Price Predictor")

# --- Load model.pkl from Google Drive ---
def load_model():
    file_id = "1G3RA7pDFouY8Ob7hpFmEH3dZ8AQDtP0u"
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url)
    return pickle.load(io.BytesIO(response.content))

try:
    model = load_model()
    st.success("✅ Model loaded successfully.")
except Exception as e:
    st.error("❌ Model loading failed.")
    st.stop()

# --- Input Fields (based on your dataset) ---
day_of_week = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
season = st.selectbox("Season", ["Winter", "Spring", "Summer", "Fall"])
location = st.selectbox("Location", ["Boston", "Chicago", "Miami", "Seattle", "Los Angeles", "New York", "San Francisco", "Austin"])
listing_type = st.selectbox("Listing Type", ["Airbnb", "Hostel", "Hotel"])
event = st.selectbox("Event Nearby", ["Yes", "No"])

base_price = st.slider("Base Price", 50, 499, 150)
demand_index = st.slider("Demand Index", 0.0, 1.0, 0.5)
competitor_avg_price = st.slider("Compet
