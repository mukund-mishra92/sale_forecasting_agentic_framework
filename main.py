from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

from app.langgraph_agent import build_sales_agent_graph
from app.state import SalesAgentState

app = FastAPI(title="Sales Forecasting Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str
    data: Optional[List[Dict]] = None  # Accepts raw sales data if uploaded

@app.post("/agent/query")
def run_agent_pipeline(query: Query):
    graph = build_sales_agent_graph()

    # Use uploaded data if provided
    if query.data:
        df = pd.DataFrame(query.data)
    else:
        from app.data_loader import load_sales_data
        df = load_sales_data()

    state = SalesAgentState(query=query.question, sales_data=df)
    result_state = graph.invoke(state)
    return {"recommendation": result_state.get("recommendation")}
