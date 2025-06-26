import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Sales Forecasting Agent", layout="centered")

st.title("📈 Sales Forecasting Agent")
st.markdown("Upload a sales CSV with `ds` (date) and `y` (sales value) columns.")

uploaded_file = st.file_uploader("Upload your sales CSV", type=["csv"])

if uploaded_file:
    try:
        # Preview uploaded data
        df = pd.read_csv(uploaded_file)
        st.write("### Preview of Uploaded Data", df.head())

        # Save temporarily and send it to FastAPI if needed later
        # Or just simulate backend POST
        df.columns = ["ds", "y"]
        df["ds"] = pd.to_datetime(df["ds"])
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()

        st.write("### Forecast Result")
        # Replace with your deployed URL or local FastAPI server
        backend_url = "http://localhost:8000/forecast"

        # Call backend (which should use the latest sales.csv)
        response = requests.get(backend_url)

        if response.status_code == 200:
            result = response.json()
            st.success("Forecast for next time step:")
            st.text_input("📅 Date", value=result["date"])
            st.text_input("📈 Predicted Value", value=round(result["predicted_value"], 2))
            st.text_input("🔻 Lower Bound", value=round(result["lower_bound"], 2))
            st.text_input("🔺 Upper Bound", value=round(result["upper_bound"], 2))
        else:
            st.error(f"API error: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
