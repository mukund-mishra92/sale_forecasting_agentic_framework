from langchain.agents import Tool
from app.forecast import forecast_sales
from app.data_loader import load_sales_data

sales_forecast_tool = Tool(
    name="SalesForecaster",
    func=lambda x: forecast_sales(load_sales_data()),
    description="Predict future sales using Prophet"
)
