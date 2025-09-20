import pandas as pd

from FlagEmbedding import FlagLLMReranker
from openai import OpenAI
from typing import Optional

from dotenv import load_dotenv
import os
import logging


logging.getLogger("transformers").setLevel(logging.ERROR)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def classify_news(news_df: pd.DataFrame, reranker_obj: Optional[object] = None) -> pd.DataFrame:
    reranker = reranker_obj
    if reranker is None:
        try:
            reranker = FlagLLMReranker('BAAI/bge-reranker-v2-gemma', use_fp16=True)
        except Exception as e:
            raise RuntimeError("Could not instantiate reranker — provide reranker_obj for tests/CI") from e

    news_df["Collaboration/Partnership"] = reranker.compute_score(
        [["Collaboration/Partnership", row["Headline"]] for _, row in news_df.iterrows()],
        normalize=True,
    )
    news_df["Industry Growth/Trends"] = reranker.compute_score(
        [["Industry Growth/Trends", row["Headline"]] for _, row in news_df.iterrows()],
        normalize=True,
    )
    news_df["Leadership Change"] = reranker.compute_score(
        [["Leadership Change", row["Headline"]] for _, row in news_df.iterrows()],
        normalize=True,
    )
    
    return news_df


def get_relevant_articles(user_goal: str, news_df: pd.DataFrame, client=None) -> pd.DataFrame:
    """
    If client_obj is provided, use it (for tests). Otherwise create a client now
    from OPENAI_API_KEY (dotenv is loaded here to support calling from arbitrary envs).
    """
    # Use injected client in tests
    if client is None:
        load_dotenv()  # idempotent, safe to call repeatedly
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set; pass client_obj in tests.")
        client = OpenAI(api_key=api_key)

    prompt = f"""
    The user has described their goal as: {user_goal}.
    
    Below are some news articles:
    {news_df["Headline"]}

    Please provide two articles that would help the user with their goal and explain why each article is relevant.
    Structure your answer exactly like this:
    1. [Write Headline here]
    [Write Reason here, around 30 words]
    """

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini",
    )
    content = completion.choices[0].message.content

    results = []
    rows = content.split("\n\n") 
    for row in rows:
        lines = row.split("\n")  
        result = {}
        if len(lines) >= 2: 
            result["Headline"] = lines[0][3:].strip('" ') 
            result["Reason"] = lines[1].strip()
            results.append(result)

    return pd.DataFrame(results)