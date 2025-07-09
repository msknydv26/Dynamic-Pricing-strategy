import streamlit as st
import pandas as pd
import pickle

# --- Load model and features ---
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("features.pkl", "rb") as f:
        features = pickle.load(f)
except FileNotFoundError:
    st.error("❌ model.pkl or features.pkl not found! Please upload both files in the same directory.")
    st.stop()

# --- Streamlit UI ---
st.set_page_config(page_title="Dynamic Pricing Predictor", page_icon="💸", layout="centered")
st.title("💸 Dynamic Pricing Strategy Predictor")
st.markdown("Enter listing details to predict the final optimal price.")

# --- Sidebar Input ---
st.sidebar.header("🛠 Input Parameters")
location = st.sidebar.selectbox("📍 Location", ["Boston", "Chicago", "Miami", "Seattle", "Los Angeles"])
listing_type = st.sidebar.selectbox("🏨 Listing Type", ["Airbnb", "Hostel"])
day_of_week = st.sidebar.selectbox("📅 Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
season = st.sidebar.selectbox("🌤️ Season", ["Winter", "Spring", "Summer", "Fall"])
event = st.sidebar.selectbox("🎉 Event Nearby?", ["Yes", "No"])

base_price = st.sidebar.number_input("💰 Base Price", 50.0, 500.0, 200.0)
demand_index = st.sidebar.slider("📈 Demand Index", 0.0, 1.0, 0.5)
competitor_avg_price = st.sidebar.number_input("📊 Competitor Avg Price", 50.0, 600.0, 250.0)
occupancy_rate = st.sidebar.slider("🏘️ Occupancy Rate (%)", 0.0, 100.0, 70.0)
customer_rating = st.sidebar.slider("⭐ Customer Rating", 0.0, 5.0, 3.5)
lead_time = st.sidebar.slider("📅 Lead Time (Days)", 0, 60, 15)
weather_score = st.sidebar.slider("🌦️ Weather Score", 0.0, 1.0, 0.5)

# --- Prepare DataFrame for Prediction ---
input_dict = {
    'base_price': base_price,
    'demand_index': demand_index,
    'competitor_avg_price': competitor_avg_price,
    'occupancy_rate': occupancy_rate,
    'customer_rating': customer_rating,
    'lead_time': lead_time,
    'weather_score': weather_score
}

# One-hot encoding
for col in features:
    if col.startswith("location_"):
        input_dict[col] = 1 if col == f"location_{location}" else 0
    elif col.startswith("listing_type_"):
        input_dict[col] = 1 if col == f"listing_type_{listing_type}" else 0
    elif col.startswith("day_of_week_"):
        input_dict[col] = 1 if col == f"day_of_week_{day_of_week}" else 0
    elif col.startswith("season_"):
        input_dict[col] = 1 if col == f"season_{season}" else 0
    elif col.startswith("event_"):
        input_dict[col] = 1 if col == f"event_{event}" else 0
    elif col not in input_dict:
        input_dict[col] = 0

input_df = pd.DataFrame([input_dict])

# --- Predict ---
if st.button("🔮 Predict Final Price"):
    price = model.predict(input_df)[0]
    st.success(f"💸 Predicted Final Price: ₹{price:.2f}")
