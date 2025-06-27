import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import sys
import os

# 📁 Add root path so we can import from app/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.forecast import analyze_time_series
from app.model_selector import recommend_model

# --- Page Setup ---
st.set_page_config(page_title="📊 Sales Forecasting Agent", layout="wide")
st.title("🤖 Sales Forecasting Agent")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "sales_df" not in st.session_state:
    st.session_state.sales_df = None

# --- Sidebar: File Upload ---
with st.sidebar:
    st.header("📂 Upload Sales Data")
    uploaded_file = st.file_uploader("Upload your sales CSV file", type=["csv"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            if "ds" in df.columns and "y" in df.columns:
                df["ds"] = pd.to_datetime(df["ds"])
                st.session_state.sales_df = df
                st.success("✅ Sales data loaded successfully!")
            else:
                st.error("❌ CSV must have columns `ds` and `y`")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
    else:
        st.info("Please upload a CSV file with 'ds' and 'y' columns.")

# --- Tabs Layout ---
tab1, tab2 = st.tabs(["💬 Forecasting Assistant", "📈 Time Series Analysis"])

# ========== TAB 1: Forecasting Assistant ==========
with tab1:
    st.subheader("💬 Ask a Forecasting or Sales Question")
    query = st.text_input("Ask me something about your sales data (e.g., 'What will my sales be for next 7 days?')")

    if query:
        with st.spinner("🤔 Thinking..."):
            try:
                # Send query to FastAPI backend
                response = requests.post("http://localhost:8000/agent/query", json={"question": query})
                if response.status_code == 200:
                    reply = response.json().get("recommendation", "")
                    if reply:
                        st.session_state.chat_history.append({"user": query, "agent": reply})
                        st.success("✅ Answer received!")
                    else:
                        st.warning("🤷 Agent returned no recommendation.")
                else:
                    st.error(f"🚨 Error from backend: {response.text}")
            except Exception as e:
                st.error(f"🔌 Could not reach backend: {e}")

    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 🧾 Conversation History")
        for chat in st.session_state.chat_history[::-1]:
            with st.expander(f"🧑 You: {chat['user']}"):
                st.markdown(f"🤖 **Agent:** {chat['agent']}")

# ========== TAB 2: Time Series Analysis ==========
with tab2:
    st.subheader("📈 Explore Trend & Seasonality")

    if st.session_state.sales_df is not None:
        df = st.session_state.sales_df
        st.line_chart(df.set_index("ds")["y"], use_container_width=True)

        period = st.number_input("Decomposition period (e.g., 7 for weekly, 12 for monthly)", min_value=2, max_value=len(df), value=7, step=1)

        if st.button("🔍 Analyze Trends"):
            with st.spinner("Analyzing trend and seasonality..."):
                try:
                    analysis = analyze_time_series(df, period)

                    st.success("✅ Analysis completed!")

                    st.markdown("### 🧠 Decomposition Components")
                    fig, ax = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
                    analysis["components"]["Trend"].plot(ax=ax[0], title="Trend")
                    analysis["components"]["Seasonal"].plot(ax=ax[1], title="Seasonality")
                    analysis["components"]["Residual"].plot(ax=ax[2], title="Residual")
                    st.pyplot(fig)

                    st.markdown("### 🔍 Model Recommendation")
                    recommendation = recommend_model(analysis)
                    st.info(f"**Recommended Model:** {recommendation}")
                except ValueError as ve:
                    st.error(f"⚠️ {ve}")
    else:
        st.info("📂 Upload a valid sales CSV to perform time series analysis.")
