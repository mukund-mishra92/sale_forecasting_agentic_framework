from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.langgraph_agent import build_sales_agent_graph
from app.state import SalesAgentState

app = FastAPI(title="Sales Forecasting Agent")

# Enable CORS if frontend like Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.get("/")
def health():
    return {"message": "Sales Forecast Agent is running!"}

@app.post("/agent/query")
def run_agent_pipeline(query: Query):
    graph = build_sales_agent_graph()
    initial_state = SalesAgentState(query=query.question)
    state = graph.invoke(initial_state)
    return {"recommendation": state.get("recommendation")}
