import pandas as pd
import numpy as np
from prophet import Prophet
from statsmodels.tsa.seasonal import seasonal_decompose
from langchain_core.runnables import Runnable
from app.state import SalesAgentState


def forecast_sales(df: pd.DataFrame, periods: int = 7):
    df = df.copy()
    df["ds"] = pd.to_datetime(df["ds"])
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]


class ForecastNode(Runnable):
    def invoke(self, state: SalesAgentState, config=None):
        print("🔸 ForecastNode received state keys:", list(state.keys()))
        if "sales_data" not in state:
            raise KeyError("❌ 'sales_data' not found in state before forecasting!")

        forecast_df = forecast_sales(state["sales_data"])
        state["forecast"] = forecast_df
        print("📈 Forecast completed.")
        return state


def analyze_time_series(df: pd.DataFrame, period: int = 7):
    if len(df) < period * 2:
        raise ValueError(f"Not enough data to decompose. Need at least {period * 2} rows, got {len(df)}.")

    df = df.sort_values("ds").copy()
    df["ds"] = pd.to_datetime(df["ds"])
    df.set_index("ds", inplace=True)

    decomposition = seasonal_decompose(df["y"], model="additive", period=period)

    trend_strength = decomposition.trend.dropna().std()
    seasonal_strength = decomposition.seasonal.dropna().std()
    residual_strength = decomposition.resid.dropna().std()

    components_df = pd.DataFrame({
        "Trend": decomposition.trend,
        "Seasonal": decomposition.seasonal,
        "Residual": decomposition.resid,
    })

    return {
        "trend_strength": trend_strength,
        "seasonality_strength": seasonal_strength,
        "residual_strength": residual_strength,
        "components": components_df
    }
