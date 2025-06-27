import pandas as pd

def parse_sales_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["ds"] = pd.to_datetime(df["ds"])
    df["y"] = df["y"].astype(float)
    return df[["ds", "y"]]