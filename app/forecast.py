from prophet import Prophet
import pandas as pd

def forecast_sales(df: pd.DataFrame):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=1)
    forecast = model.predict(future)
    #print(forecast.column())
    print(forecast)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
