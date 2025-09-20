import streamlit as st
import pandas as pd

from news_scraper import fetch_news
from ai_models import classify_news, get_relevant_articles

# --- Streamlit Application ---

st.set_page_config(layout="wide")

st.title("News Classification and Analysis")

st.write("Welcome to the News Classification Demo! Enter search terms to find and analyze news articles.")

# --- 1. User Input for Search Terms ---
search_input = st.text_input("Enter search term:", "Microsoft")
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
    user_goal_option = st.radio("Do you have a specific goal in mind?", ("No", "Yes"))

    if user_goal_option == "Yes":
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
    else:
        # --- 3. General Classification and Sorting ---
        st.header("General News Classification")
        
        # Only classify news if it hasn't been classified yet
        if 'classified_df' not in st.session_state:
            with st.spinner("Classifying headlines..."):
                st.session_state.classified_df = classify_news(st.session_state.news_df.copy())

        sort_option = st.selectbox(
            "Sort by:",
            ("Collaboration/Partnership", "Industry Growth/Trends", "Leadership Change")
        )

        if 'classified_df' in st.session_state and sort_option:
            sorted_df = st.session_state.classified_df.sort_values(by=sort_option, ascending=False)
            
            st.subheader("Top 10 Articles")
            st.dataframe(sorted_df.drop(columns="Source URL").head(10))