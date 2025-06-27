from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from app.state import SalesAgentState
from app.data_loader_node import DataLoaderNode  # ✅ Only from here
from app.forecast import ForecastNode            # ✅ Only from here
from app.llm_recommender import ask_sales_recommendation


# User input handler
class UserInputNode(Runnable):
    def invoke(self, state: SalesAgentState, config=None):
        print("📥 UserInputNode invoked with state:", state)
        return state  # Pass along input

# class DataLoaderNode(Runnable):
#     def invoke(self, state: SalesAgentState, config=None):
#         df = load_sales_data()
#         print("✅ Loaded sales data:\n", df.head())
#         state["sales_data"] = df
#         print("📦 Setting state['sales_data']")
#         return state

# Forecast node
    
# why i am getting this error here forecast_df = forecast_sales(state["sales_data"])
# KeyError: 'sales_data'
# class ForecastNode(Runnable):
#     def invoke(self, state: SalesAgentState, config=None):
#         forecast_df = forecast_sales(state["sales_data"])
#         state["forecast"] = forecast_df
#         return state

# LLM Recommender
# class LLMRecommenderNode(Runnable):
#     def invoke(self, state: SalesAgentState, config=None):
#         question = state["query"]
#         answer = ask_sales_recommendation(question)
#         state["recommendation"] = answer
#         return state
    
# class LLMRecommenderNode(Runnable):
#     def invoke(self, state: SalesAgentState, config=None):
#         print("🔸 LLMRecommenderNode invoked with keys:", list(state.keys()))
#         question = state.get("query", "")
#         if not question:
#             raise ValueError("❌ 'query' missing in state for LLM recommendation.")
#         if "forecast" not in state:
#             raise KeyError("❌ 'forecast' missing in state for LLM recommendation.")
        
#         answer = ask_sales_recommendation(state, question)
#         state["llm_response"] = answer
#         return state
    
class LLMRecommenderNode(Runnable):
    def invoke(self, state: SalesAgentState, config=None) -> SalesAgentState:
        print("🔸 LLMRecommenderNode invoked with keys:", list(state.keys()))

        question = state["query"]
        answer = ask_sales_recommendation(state, question)  # 🚨 this returns str

        print("🤖 Final recommendation:", answer)

        # ✅ Fix: Save the answer back to the state
        state["recommendation"] = answer
        return state

def build_sales_agent_graph():
    graph = StateGraph(SalesAgentState)

    graph.add_node("UserInput", UserInputNode())
    graph.add_node("LoadData", DataLoaderNode())
    graph.add_node("Forecast", ForecastNode())
    graph.add_node("LLMReasoning", LLMRecommenderNode())

    graph.set_entry_point("UserInput")
    graph.add_edge("UserInput", "LoadData")
    graph.add_edge("LoadData", "Forecast")
    graph.add_edge("Forecast", "LLMReasoning")
    graph.add_edge("LLMReasoning", END)

    return graph.compile()
