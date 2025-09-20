# News Classification

News Classification is a Streamlit application that allows users to fetch, classify, and analyze news articles based on search terms and user-specific goals. The app leverages AI models to provide goal-oriented recommendations and general news classification.


## Features

- Fetch news articles based on user-provided search terms.
- Optional goal-oriented analysis to retrieve the most relevant articles for a specific user objective.
- Classify articles into predefined categories:
  - Collaboration/Partnership
  - Industry Growth/Trends
  - Leadership Change
- Sort articles based on classification scores.

## Installation

### Prerequisites

- Python 3.12.8
- Poetry
- OpenAI API Key

### Clone the Repository

```bash
  git clone https://github.com/TheJgod/news_classification.git
  cd news-classification-demo
```

### Install Dependencies

```bash
  poetry install
```

### Environment Variables

Create a .env file in the project root and add OpenAI API key:

```bash
  OPENAI_API_KEY=<your-openai-api-key>
```

## Running the Application

### Step 1: Start the Streamlit App

```bash
  poetry run streamlit run src/news_classification/streamlit_app.py
```

- The frontend will be available at: http://localhost:8501

### Step 2: Use the Demo

1. Enter a search term to fetch news articles.
2. Choose whether you have a specific goal.
3. If a goal is provided, the demo finds relevant articles.
4. If no goal is provided, the demo classifies articles and allows sorting by category.

## Agent Architecture and Decision-Making Process

The system uses two key AI models:

1. FlagLLMReranker (BAAI/bge-reranker-v2-gemma)
   - Ranks news articles based on relevance to predefined categories.
   - Used in classify_news() to compute relevance scores for each category.
3. OpenAI GPT-4o-mini
   - Processes user goals and retrieves relevant articles.
   - Used in get_relevant_articles() to select articles aligned with user objectives.

## Running Tests

```bash
  poetry run pytest
```

## Project Structure

```bash
├── poetry.lock
├── pyproject.toml
├── src/
│   └── news_classification/
│       ├── ai_models.py        
│       ├── news_scraper.py     
│       └── streamline_app.py 
├── tests/
│   ├── test_news_scraper.py
│   └── test_ai_models.py
└── README.md
```






