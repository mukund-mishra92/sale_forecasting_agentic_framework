import pandas as pd

def load_sales_data(path: str = "/Users/balmukundmishra/Desktop/2025-Learning/ML-Course/Agent_Simple_Forecast/data/sales.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = ["ds", "y"]  # Prophet requires these column names
    df["ds"] = pd.to_datetime(df["ds"])
    return df
