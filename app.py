import streamlit as st
import pandas as pd
import traceback
import pickle

# --- Page Config ---
st.set_page_config(page_title="Dynamic Pricing Predictor", page_icon="💸", layout="centered")

# --- Title & Description ---
st.title("💸 Dynamic Pricing Strategy Predictor")
st.markdown("Use your custom-trained model to predict the **final optimal price** based on the input data.")

# --- File Uploader ---
uploaded_model = st.file_uploader("📦 Upload your trained model (.pkl)", type=["pkl"])
uploaded_csv = st.file_uploader("📄 Upload input data (.csv)", type=["csv"])

# --- Load Model ---
def load_model(file):
    try:
        model = pickle.load(file)
        return model
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        st.text(traceback.format_exc())
        return None

# --- Make Predictions ---
def make_prediction(model, df):
    try:
        prediction = model.predict(df)
        return prediction
    except Exception as e:
        st.error("❌ Prediction failed. Check if the input features match the model training data.")
        st.text(traceback.format_exc())
        return None

# --- Main App Logic ---
if uploaded_model and uploaded_csv:
    model = load_model(uploaded_model)

    if model:
        try:
            df = pd.read_csv(uploaded_csv)
            st.subheader("📊 Input Data Preview")
            st.dataframe(df.head())

            if st.button("🚀 Predict Optimal Prices"):
                with st.spinner("Predicting..."):
                    prediction = make_prediction(model, df)

                    if prediction is not None:
                        st.success("✅ Prediction Successful!")
                        df["Predicted Price"] = prediction
                        st.subheader("📈 Results")
                        st.dataframe(df)

                        # Download result
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("⬇️ Download Results", data=csv, file_name="predicted_prices.csv", mime="text/csv")

        except Exception as e:
            st.error("❌ Failed to process input CSV.")
            st.text(traceback.format_exc())

elif not uploaded_model or not uploaded_csv:
    st.info("⬆️ Please upload both the model and input data to proceed.")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | © 2025 Dynamic Pricing Predictor")
