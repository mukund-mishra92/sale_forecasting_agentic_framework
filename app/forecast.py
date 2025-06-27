# from prophet import Prophet
# import pandas as pd

# def forecast_sales(df: pd.DataFrame):
#     model = Prophet()
#     model.fit(df)
#     future = model.make_future_dataframe(periods=1)
#     forecast = model.predict(future)
#     #print(forecast.column())
#     print(forecast)
#     return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

from prophet import Prophet
import pandas as pd
from langchain_core.runnables import Runnable
from app.state import SalesAgentState

# class ForecastNode(Runnable):
#     def invoke(self, input: SalesAgentState, config=None):
#         forecast_df = forecast_sales(input['sales_data'])
#         input['forecast'] = forecast_df
#         return input

class ForecastNode(Runnable):
    def invoke(self, state: SalesAgentState, config=None):
        print("🔸 ForecastNode received state keys:", list(state.keys()))
        if "sales_data" not in state:
            raise KeyError("❌ 'sales_data' not found in state before forecasting!")

        forecast_df = forecast_sales(state["sales_data"])
        state["forecast"] = forecast_df
        print("📈 Forecast completed.")
        return state



# def forecast_sales(df: pd.DataFrame):
#     model = Prophet()
#     model.fit(df)
#     future = model.make_future_dataframe(periods=7)
#     forecast = model.predict(future)
#     return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
def forecast_sales(df: pd.DataFrame):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    print("📈 Forecast Output:\n", result.tail(10))  # Add this
    return result


