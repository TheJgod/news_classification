import streamlit as st
import pandas as pd

from news_scraper import fetch_news
from ai_models import get_relevant_articles

# --- Streamlit Application ---

st.set_page_config(layout="wide")

st.title("News Classification")

st.write("Welcome to the News Classification Demo! Enter search terms to find and analyze news articles.")

# --- 1. User Input for Search Terms ---
search_input = st.text_input("Enter search term:", "Criteo")
if "last_search_term" not in st.session_state:
    st.session_state.last_search_term = search_input
if search_input != st.session_state.last_search_term:
    st.session_state.pop("news_df", None)
    st.session_state.pop("classified_df", None)
    st.session_state.last_search_term = search_input
search_term = search_input

max_articles = st.slider("Maximum number of articles to fetch:", 10, 50, 20)

if st.button("Fetch and Analyze News"):
    if not search_term:
        st.error("Please enter at least one search term.")
    else:
        with st.spinner("Fetching news articles..."):
            news_df = fetch_news(search_term, max_articles)

        if news_df.empty:
            st.warning("No articles found! Try different search terms.")
        else:
            st.session_state.news_df = news_df
            st.success(f"{len(news_df)} articles fetched successfully!")

# --- 2. Goal-Oriented Analysis ---
if 'news_df' in st.session_state:
    st.header("Goal-Oriented Analysis")

    user_goal = st.text_input("Please describe your goal or what you are looking for:", 'lawsuit')
    if st.button("Find Relevant Articles"):
        if user_goal:
            with st.spinner("Finding relevant articles based on your goal..."):
                relevant_articles = get_relevant_articles(user_goal, st.session_state.news_df)
            
            st.subheader("Relevant Articles for Your Goal")
            for _, article in relevant_articles.iterrows():
                st.markdown(f"**Headline:** {article['Headline']}")
                st.markdown(f"**Reason:** {article['Reason']}")
                st.markdown("---")
        else:
            st.warning("Please enter your goal to find relevant articles.")
