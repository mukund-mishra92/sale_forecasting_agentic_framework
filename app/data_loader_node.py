from langchain_core.runnables import Runnable
from app.state import SalesAgentState
from app.data_loader import load_sales_data

class DataLoaderNode(Runnable):
    def invoke(self, state: SalesAgentState, config=None):
        df = load_sales_data()
        print("✅ Loaded sales data:\n", df.head())

        # ✅ Add this line — this is where your bug likely is
        state["sales_data"] = df

        print("📦 Setting state['sales_data']")
        return state
