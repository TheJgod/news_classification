FROM python:3.12.8-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=on \
    DATA_DIR=/data

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==2.2.0"

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-root --no-interaction --no-ansi

COPY src ./src

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health 

ENTRYPOINT ["poetry", "run", "streamlit", "run", "src/news_classification/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
