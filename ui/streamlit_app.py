# import streamlit as st
# import requests

# st.set_page_config(page_title="📊 Forecasting Agent", layout="centered")
# st.title("🤖 Sales Forecasting Query Assistant")

# st.markdown("""
# Ask questions like:
# - *Should I increase inventory next week?*
# - *Is there a downward trend in sales?*
# - *What are my sales for the next 7 days?*
# """)

# query = st.text_input("💬 Enter your business question")

# if query:
#     with st.spinner("Thinking..."):
#         try:
#             response = requests.post("http://localhost:8000/agent/query", json={"question": query})
#             if response.status_code == 200:
#                 st.success("✅ Agent Response:")
#                 st.markdown(f"**{response.json()['recommendation']}**")
#             else:
#                 st.error(f"❌ Error from agent: {response.text}")
#         except Exception as e:
#             st.error(f"Connection error: {str(e)}")


import streamlit as st
import requests

st.set_page_config(page_title="📊 Forecasting Agent", layout="centered")
st.title("🤖 Sales Forecasting Query Assistant")

st.markdown("""
Ask questions like:
- *Should I increase inventory next week?*
- *Is there a downward trend in sales?*
- *What are my sales for the next 7 days?*
""")

query = st.text_input("💬 Enter your business question")

if query:
    with st.spinner("Thinking..."):
        try:
            response = requests.post("http://localhost:8000/agent/query", json={"question": query})
            
            if response.status_code == 200:
                response_data = response.json()

                # Support both expected formats just in case
                recommendation = response_data.get("recommendation") or response_data.get("output") or str(response_data)

                st.success("✅ Agent Response:")
                st.markdown(f"**{recommendation}**")

            else:
                st.error(f"❌ Error from agent: {response.text}")
        except Exception as e:
            st.error(f"⚠️ Connection error: {str(e)}")
