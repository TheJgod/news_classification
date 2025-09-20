# tests/test_ai_models_di.py
import pandas as pd
import src.news_classification.ai_models as ai_models
import types
import os
import pytest

class FakeReranker:
    def compute_score(self, pairs, normalize=True):
        return [float(len(headline)) for _, headline in pairs]

def test_classify_news_with_fake_reranker():
    df = pd.DataFrame({"Headline": ["First headline", "Second"]})
    fake = FakeReranker()
    out = ai_models.classify_news(df.copy(), reranker_obj=fake)
    expected = [float(len(h)) for h in df["Headline"]]
    assert out["Collaboration/Partnership"].tolist() == expected

def test_classify_news_with_empty_dataframe():
    df = pd.DataFrame(columns=["Headline"])
    fake = FakeReranker()
    out = ai_models.classify_news(df.copy(), reranker_obj=fake)

    # Should preserve shape and add new columns
    assert list(out.columns) == ["Headline", "Collaboration/Partnership", "Industry Growth/Trends", "Leadership Change"]
    assert out.empty

def make_fake_response(text):
    return types.SimpleNamespace(
        choices=[types.SimpleNamespace(message=types.SimpleNamespace(content=text))]
    )

def test_get_relevant_articles_with_injected_client():
    sample_content = (
        '1. "Article A"\n'
        "Reason A around thirty words explaining why.\n\n"
        '2. "Article B"\n'
        "Reason B around thirty words explaining why.\n"
    )
    fake_resp = make_fake_response(sample_content)
    fake_client = types.SimpleNamespace(
        chat=types.SimpleNamespace(
            completions=types.SimpleNamespace(
                create=lambda messages, model: fake_resp
            )
        )
    )

    news_df = pd.DataFrame({"Headline": ["Article A", "Article B"]})
    out = ai_models.get_relevant_articles("User goal", news_df, client=fake_client)

    assert len(out) == 2
    assert out.loc[0, "Headline"] == "Article A"
    assert "Reason A" in out.loc[0, "Reason"] or len(out.loc[0, "Reason"]) > 0

def test_get_relevant_articles_raises_if_no_api_key(monkeypatch):
    monkeypatch.setattr(os, "getenv", lambda key: None) 
    news_df = pd.DataFrame({"Headline": ["A"]})

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY not set"):
        ai_models.get_relevant_articles("Goal", news_df)
        
def test_get_relevant_articles_with_empty_news_df():
    sample_content = ""  
    fake_resp = make_fake_response(sample_content)
    fake_client = types.SimpleNamespace(
        chat=types.SimpleNamespace(
            completions=types.SimpleNamespace(
                create=lambda messages, model: fake_resp
            )
        )
    )

    news_df = pd.DataFrame({"Headline": []})
    out = ai_models.get_relevant_articles("Some goal", news_df, client=fake_client)
    assert out.empty
