import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import io

# --- Streamlit Config ---
st.set_page_config(page_title="PWAVE: Dynamic Pricing Predictor", page_icon="💸", layout="centered")
st.title("💸 PWAVE: Dynamic Pricing Strategy Predictor")
st.markdown("Use interactive filters to simulate and predict optimal pricing.")

# --- Load model.pkl from Google Drive ---
@st.cache_resource
def load_model_from_drive():
    try:
        file_id = "1G3RA7pDFouY8Ob7hpFmEH3dZ8AQDtP0u"
        url = f"https://drive.google.com/uc?id={file_id}"
        response = requests.get(url)
        response.raise_for_status()
        return pickle.load(io.BytesIO(response.content))
    except Exception as e:
        st.error(f"❌ Failed to load model from Drive: {e}")
        return None

model = load_model_from_drive()

# --- Define Features (based on your dataset) ---
features = {
    "day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "season": ["Winter", "Spring", "Summer", "Fall"],
    "location": ["Boston", "Chicago", "Miami", "Seattle", "Los Angeles", "New York", "San Francisco", "Austin"],
    "listing_type": ["Airbnb", "Hostel", "Hotel"],
    "base_price": (50, 499),
    "demand_index": (0.0, 1.0),
    "competitor_avg_price": (40, 597),
    "occupancy_rate": (30, 100),
    "event": ["Yes", "No"],
    "customer_rating": (3.0, 5.0),
    "lead_time": (0, 59),
    "weather_score": (0.0, 1.0),
    "discount_offered": (0.0, 20.0)
}

# --- UI Inputs ---
if model:
    st.success("✅ Model loaded successfully.")
    st.subheader("📋 Input Parameters")

    user_inputs = {}
    for feature, val in features.items():
        if isinstance(val, list):
            user_inputs[feature] = st.selectbox(f"{feature.replace('_', ' ').title()}:", val)
        elif isinstance(val, tuple):
            min_val, max_val = val
            if isinstance(min_val, float) or isinstance(max_val, float):
                user_inputs[feature] = st.slider(f"{feature.replace('_', ' ').title()}:", float(min_val), float(max_val), float((min_val + max_val) / 2))
            else:
                user_inputs[feature] = st.slider(f"{feature.replace('_', ' ').title()}:", int(min_val), int(max_val), int((min_val + max_val) / 2))
        else:
            user_inputs[feature] = st.text_input(f"{feature.replace('_', ' ').title()}:")

    if st.button("🚀 Predict Price"):
        try:
            input_df = pd.DataFrame([user_inputs])
            prediction = model.predict(input_df)[0]
            st.success(f"💰 Predicted Optimal Price: ₹ {round(prediction, 2)}")
        except Exception as e:
            st.error("❌ Prediction failed.")
            st.text(str(e))
else:
    st.warning("⚠️ Model could not be loaded. Please check the Drive link or file permissions.")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ by Team PWAVE | Powered by Streamlit + ML")
