{"schemaVersion":1,"label":"tests","message":"3 passed","color":"brightgreen"}

# News Classification

News Classification is a Streamlit application that allows users to fetch, classify, and analyze news articles based on search terms and user-specific goals. The app leverages AI models to provide goal-oriented recommendations.


## Features

- Fetch news articles based on user-provided search terms.
- Goal-oriented analysis to retrieve the most relevant articles for a specific user objective.

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
2. Specify a goal.
3. The demo finds relevant articles.

## Agent Architecture and Decision-Making Process

The system uses:

1. OpenAI GPT-4o-mini
   - Processes user goals and retrieves relevant articles.
   - Used in get_relevant_articles() to select articles aligned with user objectives.

## Running Tests

```bash
  poetry run pytest
```

## Docker Deployment

Build image:

```bash
  docker build -t news-classification .
```

Run:

```bash
  docker run -p 8501:8501 --env-file .env news-classification
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










