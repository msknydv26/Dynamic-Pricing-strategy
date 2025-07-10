import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import io

# --- App Setup ---
st.set_page_config(page_title="PWAVE - Dynamic Pricing Predictor", page_icon="💸", layout="centered")
st.title("💸 PWAVE: Dynamic Pricing Strategy Predictor")
st.markdown("Predict optimal prices dynamically using your trained ML model and interactive inputs.")

# --- Load features.pkl from local repo ---
@st.cache_data
def load_local_features():
    try:
        with open("features.pkl", "rb") as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"❌ Failed to load features.pkl: {e}")
        return None

# --- Load model.pkl from Google Drive ---
@st.cache_resource
def load_model_from_drive():
    try:
        file_id = "1G3RA7pDFouY8Ob7hpFmEH3dZ8AQDtP0u"  # Your file ID
        download_url = f"https://drive.google.com/uc?id={file_id}"
        response = requests.get(download_url)
        response.raise_for_status()
        return pickle.load(io.BytesIO(response.content))
    except Exception as e:
        st.error(f"❌ Error loading model from Google Drive: {e}")
        return None

# --- Load files ---
features = load_local_features()
model = load_model_from_drive()

# --- Main App Logic ---
if model and features:
    st.success("✅ Model and feature schema loaded successfully.")
    st.subheader("🎛️ Input Parameters")

    input_data = {}
    for feature, options in features.items():
        if isinstance(options, list):
            input_data[feature] = st.selectbox(f"{feature}:", options)
        elif isinstance(options, tuple) and len(options) == 2:
            min_val, max_val = options
            input_data[feature] = st.slider(f"{feature}:", min_val, max_val, value=(min_val + max_val) // 2)
        else:
            input_data[feature] = st.text_input(f"{feature}:")

    # Prediction
    if st.button("🚀 Predict"):
        try:
            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]
            st.success(f"💰 Predicted Optimal Price: ₹ {round(prediction, 2)}")
        except Exception as e:
            st.error("❌ Prediction failed.")
            st.text(str(e))
else:
    st.warning("⚠️ Please ensure that both the model and features are correctly loaded.")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ by Team PWAVE | Powered by Streamlit")
