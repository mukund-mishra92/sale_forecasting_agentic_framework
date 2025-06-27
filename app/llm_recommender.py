import os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from app.forecast import forecast_sales
from app.data_loader import load_sales_data

from langchain_experimental.agents import create_pandas_dataframe_agent
#from langchain_community.llms import OpenAI  # ✅ updated import
from langchain_openai import OpenAI

# def get_combined_dataframe():
#     raw_df = load_sales_data()
#     forecast_df = forecast_sales(raw_df)
#     combined = pd.merge(raw_df.tail(7), forecast_df.tail(7), on="ds", how="outer")
#     return combined

# def get_combined_dataframe(state: dict) -> pd.DataFrame:
#     raw_df = state["sales_data"]
#     forecast_df = state["forecast"]

#     # 🔧 Ensure datetime
#     raw_df['ds'] = pd.to_datetime(raw_df['ds'])
#     forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])

#     # Use concat instead of merge to avoid key mismatches
#     combined = pd.concat([raw_df.tail(7), forecast_df.tail(7)], ignore_index=True)

#     print("🧩 Combined DataFrame:\n", combined.tail(10))
#     return combined

def get_combined_dataframe(state: dict) -> pd.DataFrame:
    raw_df = state["sales_data"]
    forecast_df = state["forecast"]

    raw_df['ds'] = pd.to_datetime(raw_df['ds'])
    forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])

    combined = pd.concat([raw_df, forecast_df], ignore_index=True)
    combined = combined.sort_values("ds")

    # ✅ Rename to make LLM understand what the data represents
    combined.rename(columns={
        "ds": "date",
        "y": "actual_sales",
        "yhat": "predicted_sales",
        "yhat_lower": "lower_bound",
        "yhat_upper": "upper_bound"
    }, inplace=True)

    return combined.tail(14)



def get_llm_recommendation_agent(state: dict):
    df = get_combined_dataframe(state)
    llm = OpenAI(temperature=0.2)
    return create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=False,
        allow_dangerous_code=True
    )

def ask_sales_recommendation(state: dict, question: str) -> str:
    df = get_combined_dataframe(state)
    print("📊 Data passed to LLM Agent:\n", df)

    llm = OpenAI(temperature=0.2)
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        allow_dangerous_code=True
    )

    response = agent.invoke(question)
    print("🤖 Agent Response:", response)
    return response

