from typing import TypedDict, Optional
import pandas as pd

class SalesAgentState(TypedDict, total=False):
    query: str
    sales_data: pd.DataFrame
    forecast: pd.DataFrame
    recommendation: str
