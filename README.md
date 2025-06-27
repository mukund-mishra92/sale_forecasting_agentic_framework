# sale_forecasting_agentic_framework

## Run the backend

### uvicorn main:app --reload

## Run the FrontEnd

### streamlit run ui/streamlit_app.py



[User Query]
     ↓
[SalesDataNode] → loads data
     ↓
[LLMNode] → decides whether to analyze raw, forecast, or both
     ↓
[ToolNode] → generates forecast (Prophet)
     ↓
[LLMNode] → generates recommendation
     ↓
[Response to User]
