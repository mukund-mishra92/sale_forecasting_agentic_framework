from fastapi import FastAPI
from app.forecast import forecast_sales
from app.data_loader import load_sales_data

app = FastAPI(title="Sales Forecasting Agent")

# @app.get("/forecast")
# def get_forecast():
#     df = load_sales_data()
#     result = forecast_sales(df)
#     return result.tail(1).to_dict(orient="records")

@app.get("/forecast")
def get_forecast():
    df = load_sales_data()
    result = forecast_sales(df)
    row = result.tail(1).to_dict(orient="records")[0]
    
    # Rename fields for better readability
    renamed = {
        "date": row["ds"],
        "predicted_value": row["yhat"],
        "lower_bound": row["yhat_lower"],
        "upper_bound": row["yhat_upper"]
    }
    
    return renamed
