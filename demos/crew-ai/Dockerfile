FROM python:3.12-slim

RUN apt-get update && apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root
COPY . .
RUN poetry install
CMD ["poetry", "run", "marketing_posts"]
